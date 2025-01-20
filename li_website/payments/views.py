from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from yookassa import Configuration, Payment as YooKassaPayment
from .models import Payment
from courses.models import Course, Purchase
import uuid
import json
import logging
import traceback

logger = logging.getLogger(__name__)

# Configure YooKassa
Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

def create_payment(request):
    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount'))
            description = request.POST.get('description', 'Payment for services')
            
            logger.info(f"Creating payment for user {request.user.id} with amount {amount}")
            
            # Create payment in YooKassa with receipt
            payment = YooKassaPayment.create({
                "amount": {
                    "value": str(amount),
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": f"{request.build_absolute_uri('/payments/complete/')}"
                },
                "capture": True,
                "description": description,
                "metadata": {
                    "user_id": request.user.id,
                    "course_title": description.replace('Оплата курса: ', '')
                },
                "receipt": {
                    "customer": {
                        "email": request.user.email  # Get email from authenticated user
                    },
                    "items": [
                        {
                            "description": description.replace('Оплата курса: ', ''),
                            "quantity": "1",
                            "amount": {
                                "value": str(amount),
                                "currency": "RUB"
                            },
                            "vat_code": "6",  # НДС не облагается
                            "payment_mode": "full_prepayment",
                            "payment_subject": "service"
                        }
                    ]
                }
            })
            
            logger.info(f"Created YooKassa payment with ID: {payment.id}")

            # Save payment to database
            db_payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                payment_id=payment.id,
                description=description,
                status='pending'
            )
            
            logger.info(f"Saved payment to database with ID: {db_payment.id}")

            return JsonResponse({'redirect_url': payment.confirmation.confirmation_url})

        except Exception as e:
            logger.error(f"Error creating payment: {str(e)}")
            logger.error(traceback.format_exc())
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
@require_http_methods(["POST"])
def payment_webhook(request):
    try:
        event_json = json.loads(request.body)
        logger.info(f"Received webhook: {event_json}")
        
        # Get payment info
        payment_id = event_json['object']['id']
        logger.info(f"Processing webhook for payment ID: {payment_id}")
        
        yookassa_payment = YooKassaPayment.find_one(payment_id)
        logger.info(f"YooKassa payment status: {yookassa_payment.status}")
        
        # Update local payment
        payment = Payment.objects.get(payment_id=payment_id)
        old_status = payment.status
        payment.status = yookassa_payment.status
        payment.save()
        logger.info(f"Updated payment status from {old_status} to {payment.status}")
        
        # If payment is successful, grant access to the course
        if yookassa_payment.status == 'succeeded':
            course_title = yookassa_payment.metadata.get('course_title')
            logger.info(f"Processing successful payment for course: {course_title}")
            
            if course_title:
                try:
                    course = Course.objects.get(title=course_title)
                    purchase, created = Purchase.objects.get_or_create(
                        user=payment.user,
                        course=course
                    )
                    logger.info(f"Created purchase (new={created}) for user {payment.user.id} and course {course.id}")
                except Course.DoesNotExist:
                    logger.error(f"Course not found: {course_title}")
                except Exception as e:
                    logger.error(f"Error creating purchase: {str(e)}")
                    logger.error(traceback.format_exc())

        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        logger.error(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=400)

def payment_complete(request):
    logger.info("Payment complete view called")
    logger.info(f"Request user: {request.user}")
    logger.info(f"Request GET params: {request.GET}")
    
    try:
        if not request.user.is_authenticated:
            logger.error("User not authenticated")
            return render(request, 'payments/complete.html', {
                'status': 'error',
                'message': 'Пожалуйста, войдите в систему'
            })

        # Find the most recent pending payment for the current user
        recent_payment = Payment.objects.filter(
            user=request.user,
            status='pending'
        ).order_by('-created_at').first()
        
        logger.info(f"Found recent payment: {recent_payment}")
        
        if recent_payment:
            # Check payment status in YooKassa
            try:
                yookassa_payment = YooKassaPayment.find_one(recent_payment.payment_id)
                logger.info(f"YooKassa payment status: {yookassa_payment.status}")
                
                # Update payment status
                recent_payment.status = yookassa_payment.status
                recent_payment.save()
                logger.info(f"Updated payment status to: {recent_payment.status}")
                
                # If payment is successful, create purchase
                if yookassa_payment.status == 'succeeded':
                    course_title = yookassa_payment.metadata.get('course_title')
                    logger.info(f"Processing successful payment for course: {course_title}")
                    
                    if course_title:
                        try:
                            course = Course.objects.get(title=course_title)
                            purchase, created = Purchase.objects.get_or_create(
                                user=request.user,
                                course=course
                            )
                            logger.info(f"Created purchase (new={created}) for course {course.id}")
                            
                            return render(request, 'payments/complete.html', {
                                'status': 'success',
                                'message': 'Оплата прошла успешно! Теперь у вас есть доступ к курсу.',
                                'course_slug': course.slug
                            })
                        except Course.DoesNotExist:
                            logger.error(f"Course not found: {course_title}")
                            return render(request, 'payments/complete.html', {
                                'status': 'error',
                                'message': 'Курс не найден. Пожалуйста, свяжитесь с поддержкой.'
                            })
                
                # Handle other payment statuses
                if yookassa_payment.status == 'pending':
                    return render(request, 'payments/complete.html', {
                        'status': 'pending',
                        'message': 'Проверяем статус оплаты...'
                    })
                else:
                    return render(request, 'payments/complete.html', {
                        'status': 'error',
                        'message': f'Статус платежа: {yookassa_payment.status}'
                    })
            except Exception as e:
                logger.error(f"Error checking YooKassa payment: {str(e)}")
                logger.error(traceback.format_exc())
                return render(request, 'payments/complete.html', {
                    'status': 'error',
                    'message': 'Ошибка при проверке платежа в YooKassa'
                })
        else:
            logger.warning("No pending payment found")
            return render(request, 'payments/complete.html', {
                'status': 'error',
                'message': 'Платеж не найден'
            })
            
    except Exception as e:
        logger.error(f"Error in payment_complete: {str(e)}")
        logger.error(traceback.format_exc())
        return render(request, 'payments/complete.html', {
            'status': 'error',
            'message': 'Произошла ошибка при проверке платежа'
        })
