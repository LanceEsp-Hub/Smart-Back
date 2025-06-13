# backend\app\routers\admin_router.py


from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi.responses import FileResponse

from app.database.database import get_db
from app.models import models


router = APIRouter(prefix="/admin", tags=["admin"])

# @router.get("/dashboard-stats")
# async def get_dashboard_stats(
#     time_range: str = Query("all", description="Time range: day, week, month, year, all"),
#     db: Session = Depends(get_db)
# ):
#     time_filters = {
#         "day": datetime.utcnow() - timedelta(days=1),
#         "week": datetime.utcnow() - timedelta(weeks=1),
#         "month": datetime.utcnow() - timedelta(days=30),
#         "year": datetime.utcnow() - timedelta(days=365),
#         "all": None
#     }
#     time_filter = time_filters.get(time_range.lower())

#     def apply_time_filter(query, column):
#         if time_filter:
#             return query.filter(column >= time_filter)
#         return query

#     # User Statistics
#     users_query = apply_time_filter(db.query(models.User), models.User.created_at)
#     total_users = users_query.count()
#     active_users = users_query.filter(models.User.is_active == True).count()
#     verified_users = users_query.filter(models.User.is_verified == True).count()

#     # Pet Statistics
#     pets_query = apply_time_filter(db.query(models.Pet), models.Pet.created_at)
#     total_pets = pets_query.count()
#     published_pets = pets_query.filter(models.Pet.is_published == True).count()
#     approved_pets = pets_query.filter(models.Pet.admin_approved == True).count()

#     # Adoption Statistics
#     adoptions_query = apply_time_filter(db.query(models.AdoptedPet), models.AdoptedPet.created_at)
#     total_adoptions = adoptions_query.count()
#     pending_adoptions = adoptions_query.filter(models.AdoptedPet.status == 'pending').count()
#     successful_adoptions = adoptions_query.filter(models.AdoptedPet.status == 'successful').count()

#     # Form Statistics
#     forms_query = apply_time_filter(db.query(models.AdoptionForm), models.AdoptionForm.created_at)
#     total_forms = forms_query.count()
#     pending_forms = forms_query.filter(models.AdoptionForm.status == 'pending').count()

#     # Message Statistics
#     messages_query = apply_time_filter(db.query(models.Message), models.Message.timestamp)
#     total_messages = messages_query.count()
#     unread_messages = messages_query.filter(models.Message.is_read == False).count()

#     return {
#         "users": {
#             "total": total_users,
#             "active": active_users,
#             "verified": verified_users,
#             "new": users_query.filter(models.User.created_at >= datetime.utcnow() - timedelta(days=7)).count()
#         },
#         "pets": {
#             "total": total_pets,
#             "published": published_pets,
#             "approved": approved_pets,
#             "by_type": {
#                 "dogs": pets_query.filter(models.Pet.type == 'dog').count(),
#                 "cats": pets_query.filter(models.Pet.type == 'cat').count(),
#                 "others": pets_query.filter(~models.Pet.type.in_(['dog', 'cat'])).count()
#             },
#             "status_distribution": {
#                 "safe": pets_query.filter(models.Pet.status == 'Safe at Home').count(),
#                 "lost": pets_query.filter(models.Pet.status == 'Lost').count(),
#                 "found": pets_query.filter(models.Pet.status == 'Found').count(),
#                 "rehome": pets_query.filter(models.Pet.status == 'Rehome Pet').count()
#             }
#         },
#         "adoptions": {
#             "total": total_adoptions,
#             "pending": pending_adoptions,
#             "successful": successful_adoptions,
#             "cancelled": total_adoptions - pending_adoptions - successful_adoptions
#         },
#         "forms": {
#             "total": total_forms,
#             "pending": pending_forms,
#             "approved": forms_query.filter(models.AdoptionForm.status == 'approved').count(),
#             "declined": forms_query.filter(models.AdoptionForm.status == 'declined').count()
#         },
#         "messages": {
#             "total": total_messages,
#             "unread": unread_messages,
#             "conversations": apply_time_filter(db.query(models.Conversation), models.Conversation.created_at).count()
#         },
#         "notifications": {
#             "total": apply_time_filter(db.query(models.UserNotification), models.UserNotification.created_at).count(),
#             "unread": apply_time_filter(db.query(models.UserNotification).filter(models.UserNotification.is_read == False), 
#                                       models.UserNotification.created_at).count()
#         }
#     }

@router.get("/dashboard-stats")
async def get_dashboard_stats(
    time_range: str = Query("all", description="Time range: day, week, month, year, all"),
    db: Session = Depends(get_db)
):
    time_filters = {
        "day": datetime.utcnow() - timedelta(days=1),
        "week": datetime.utcnow() - timedelta(weeks=1),
        "month": datetime.utcnow() - timedelta(days=30),
        "year": datetime.utcnow() - timedelta(days=365),
        "all": None
    }
    time_filter = time_filters.get(time_range.lower())

    def apply_time_filter(query, column):
        if time_filter:
            return query.filter(column >= time_filter)
        return query

    # User Statistics
    users_query = apply_time_filter(db.query(models.User), models.User.created_at)
    total_users = users_query.count()
    active_users = users_query.filter(models.User.is_active == True).count()
    verified_users = users_query.filter(models.User.is_verified == True).count()

    # Pet Statistics
    pets_query = apply_time_filter(db.query(models.Pet), models.Pet.created_at)
    total_pets = pets_query.count()
    published_pets = pets_query.filter(models.Pet.is_published == True).count()
    approved_pets = pets_query.filter(models.Pet.admin_approved == True).count()

    # Adoption Statistics
    adoptions_query = apply_time_filter(db.query(models.AdoptedPet), models.AdoptedPet.created_at)
    total_adoptions = adoptions_query.count()
    pending_adoptions = adoptions_query.filter(models.AdoptedPet.status == 'pending').count()
    successful_adoptions = adoptions_query.filter(models.AdoptedPet.status == 'successful').count()

    # Form Statistics
    forms_query = apply_time_filter(db.query(models.AdoptionForm), models.AdoptionForm.created_at)
    total_forms = forms_query.count()
    pending_forms = forms_query.filter(models.AdoptionForm.status == 'pending').count()

    # Login Statistics
    login_logs_query = apply_time_filter(db.query(models.LoginLog), models.LoginLog.created_at)
    total_logins = login_logs_query.count()
    failed_logins = login_logs_query.filter(models.LoginLog.status != 'success').count()

    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "verified": verified_users,
            "new": users_query.filter(models.User.created_at >= datetime.utcnow() - timedelta(days=7)).count(),
            "deactivated": users_query.filter(models.User.deactivated_at.isnot(None)).count()
        },
        "pets": {
            "total": total_pets,
            "published": published_pets,
            "approved": approved_pets,
            "with_fingerprints": pets_query.filter(models.Pet.has_generated_fingerprint == True).count(),
            "by_type": {
                "dogs": pets_query.filter(models.Pet.type == 'dog').count(),
                "cats": pets_query.filter(models.Pet.type == 'cat').count(),
                "others": pets_query.filter(~models.Pet.type.in_(['dog', 'cat'])).count()
            },
            "status_distribution": {
                "safe": pets_query.filter(models.Pet.status == 'Safe at Home').count(),
                "lost": pets_query.filter(models.Pet.status == 'Lost').count(),
                "found": pets_query.filter(models.Pet.status == 'Found').count(),
                "rehome": pets_query.filter(models.Pet.status == 'Rehome Pet').count()
            }
        },
        "adoptions": {
            "total": total_adoptions,
            "pending": pending_adoptions,
            "successful": successful_adoptions,
            "cancelled": adoptions_query.filter(models.AdoptedPet.status == 'cancelled').count()
        },
        "forms": {
            "total": total_forms,
            "pending": pending_forms,
            "approved": forms_query.filter(models.AdoptionForm.status == 'approved').count(),
            "declined": forms_query.filter(models.AdoptionForm.status == 'declined').count()
        },
        "security": {
            "total_logins": total_logins,
            "failed_logins": failed_logins,
            "suspicious_activity": login_logs_query.filter(
                models.LoginLog.status == 'suspicious'
            ).count()
        },
        "pet_similarity": {
            "total_searches": db.query(models.PetSimilaritySearch).count(),
            "successful_matches": db.query(models.PetSimilaritySearch).filter(
                models.PetSimilaritySearch.was_successful == True
            ).count()
        }
    }

@router.get("/recent-activity")
async def get_recent_activity(db: Session = Depends(get_db)):
    recent_users = db.query(models.User)\
        .order_by(models.User.created_at.desc())\
        .limit(5)\
        .all()
    
    recent_pets = db.query(models.Pet)\
        .order_by(models.Pet.created_at.desc())\
        .limit(5)\
        .all()
    
    recent_adoptions = db.query(models.AdoptedPet)\
        .order_by(models.AdoptedPet.created_at.desc())\
        .limit(5)\
        .all()
    
    recent_forms = db.query(models.AdoptionForm)\
        .order_by(models.AdoptionForm.created_at.desc())\
        .limit(5)\
        .all()
    
    return {
        "users": [
            {"id": u.id, "name": u.name, "email": u.email, "created_at": u.created_at} 
            for u in recent_users
        ],
        "pets": [
            {"id": p.id, "name": p.name, "type": p.type, "status": p.status, "created_at": p.created_at} 
            for p in recent_pets
        ],
        "adoptions": [
            {"id": a.id, "pet_id": a.pet_id, "status": a.status, "created_at": a.created_at} 
            for a in recent_adoptions
        ],
        "forms": [
            {"id": f.id, "user_id": f.user_id, "status": f.status, "created_at": f.created_at} 
            for f in recent_forms
        ]
    }



@router.get("/pet-management")
async def get_pets_for_management(
    status: str = Query("pending", description="Filter by approval status: pending, approved, rejected"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    # Base query with join to get owner information
    query = db.query(
        models.Pet,
        models.User.name.label("owner_name"),
        models.User.email.label("owner_email")
    ).join(
        models.User, models.Pet.user_id == models.User.id
    )
    
    # Apply status filter
    if status == "pending":
        query = query.filter(models.Pet.admin_approved == False)
    elif status == "approved":
        query = query.filter(models.Pet.admin_approved == True)
    elif status == "rejected":
        query = query.filter(models.Pet.admin_approved == False, models.Pet.is_published == False)
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination and ordering
    pets = query.order_by(models.Pet.created_at.desc())\
               .offset((page - 1) * limit)\
               .limit(limit)\
               .all()
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "status": status,
        "data": [{
            "id": pet.Pet.id,
            "name": pet.Pet.name,
            "type": pet.Pet.type,
            "gender": pet.Pet.gender,
            "description": pet.Pet.description,
            "address": pet.Pet.address,
            "status": pet.Pet.status,
            "user_id": pet.Pet.user_id,
            "owner_name": pet.owner_name,
            "owner_email": pet.owner_email,
            "created_at": pet.Pet.created_at.isoformat(),
            "image": pet.Pet.image,
            "additional_images": pet.Pet.additional_images,
            "admin_approved": pet.Pet.admin_approved,
            "is_published": pet.Pet.is_published,
            "has_generated_fingerprint": pet.Pet.has_generated_fingerprint,
            "latitude": pet.Pet.latitude,
            "longitude": pet.Pet.longitude,
            # Health info if needed
            "health_info": {
                "vaccinated": pet.Pet.health_info.vaccinated if pet.Pet.health_info else None,
                "spayed_neutered": pet.Pet.health_info.spayed_neutered if pet.Pet.health_info else None,
                "energy_level": pet.Pet.health_info.energy_level if pet.Pet.health_info else None
            } if hasattr(pet.Pet, 'health_info') else None
        } for pet in pets]
    }

@router.patch("/pet-management/{pet_id}")
async def manage_pet(
    pet_id: int,
    action: str = Query(..., description="Action to perform: approve, reject, unpublish"),
    db: Session = Depends(get_db)
):
    pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    if action == "approve":
        pet.admin_approved = True
        pet.is_published = True
        message = "Pet approved and published"
    elif action == "reject":
        pet.admin_approved = False
        pet.is_published = False
        message = "Pet rejected"
    elif action == "unpublish":
        pet.is_published = False
        message = "Pet unpublished"
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    db.commit()
    
    return {"success": True, "message": message}



# @router.get("/users")
# async def get_users_for_admin(
#     page: int = Query(1, ge=1),
#     limit: int = Query(10, ge=1, le=100),
#     search: str = Query(None),
#     db: Session = Depends(get_db)
# ):
#     # Base query with joins
#     query = db.query(
#         models.User,
#         models.Address,
#         models.Notification
#     ).outerjoin(
#         models.Address, models.User.address_id == models.Address.id
#     ).outerjoin(
#         models.Notification, models.User.notification_id == models.Notification.id
#     ).filter(
#         models.User.roles == "user"  # Only get regular users
#     ).order_by(
#         models.User.created_at.desc()
#     )

#     # Apply search filter if provided
#     if search:
#         query = query.filter(
#             or_(
#                 models.User.name.ilike(f"%{search}%"),
#                 models.User.email.ilike(f"%{search}%"),
#                 models.User.phone_number.ilike(f"%{search}%")
#             )
#         )

#     # Get total count before pagination
#     total = query.count()
    
#     # Apply pagination
#     users = query.offset((page - 1) * limit).limit(limit).all()

#     return {
#         "total": total,
#         "page": page,
#         "limit": limit,
#         "data": [{
#             "id": user.User.id,
#             "name": user.User.name,
#             "email": user.User.email,
#             "is_active": user.User.is_active,
#             "is_verified": user.User.is_verified,
#             "deactivated_at": user.User.deactivated_at.isoformat() if user.User.deactivated_at else None,
#             "created_at": user.User.created_at.isoformat(),
#             "profile_picture": user.User.profile_picture,
#             "phone_number": user.User.phone_number,
#             "address": {
#                 "street": user.Address.street if user.Address else None,
#                 "city": user.Address.city if user.Address else None,
#                 "state": user.Address.state if user.Address else None,
#                 "country": user.Address.country if user.Address else None
#             },
#             "notification_settings": {
#                 "email_notifications": user.Notification.account_updates if user.Notification else None,
#                 "push_notifications": user.Notification.push_notifications if user.Notification else None
#             }
#         } for user in users]
#     }

@router.get("/users")
async def get_users_for_admin(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    # Base query with joins
    query = db.query(
        models.User,
        models.Address,
        models.Notification
    ).outerjoin(
        models.Address, models.User.address_id == models.Address.id
    ).outerjoin(
        models.Notification, models.User.notification_id == models.Notification.id
    ).filter(
        models.User.roles == "user"  # Only get regular users
    ).order_by(
        models.User.created_at.desc()
    )

    # Apply search filter if provided
    if search:
        query = query.filter(
            or_(
                models.User.name.ilike(f"%{search}%"),
                models.User.email.ilike(f"%{search}%"),
                models.User.phone_number.ilike(f"%{search}%")
            )
        )

    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    users = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": [{
            "id": user.User.id,
            "name": user.User.name,
            "email": user.User.email,
            "is_active": user.User.is_active,
            "is_verified": user.User.is_verified,
            "account_status": user.User.account_status,  # Added account_status here
            "deactivated_at": user.User.deactivated_at.isoformat() if user.User.deactivated_at else None,
            "created_at": user.User.created_at.isoformat(),
            "profile_picture": user.User.profile_picture,
            "phone_number": user.User.phone_number,
            "address": {
                "street": user.Address.street if user.Address else None,
                "city": user.Address.city if user.Address else None,
                "state": user.Address.state if user.Address else None,
                "country": user.Address.country if user.Address else None
            },
            "notification_settings": {
                "email_notifications": user.Notification.account_updates if user.Notification else None,
                "push_notifications": user.Notification.push_notifications if user.Notification else None
            }
        } for user in users]
    }

@router.get("/pet-health")
async def get_pet_health_records(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    # Base query with join to get pet information
    query = db.query(
        models.PetHealth,
        models.Pet.name.label("pet_name"),
        models.Pet.type.label("pet_type"),
        models.Pet.status.label("pet_status"),
        models.User.name.label("owner_name")
    ).join(
        models.Pet, models.PetHealth.pet_id == models.Pet.id
    ).join(
        models.User, models.Pet.user_id == models.User.id
    ).order_by(
        models.PetHealth.updated_at.desc()
    )

    # Apply search filter if provided
    if search:
        query = query.filter(
            or_(
                models.Pet.name.ilike(f"%{search}%"),
                models.User.name.ilike(f"%{search}%"),
                models.PetHealth.health_details.ilike(f"%{search}%")
            )
        )

    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    health_records = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": [{
            "pet_id": record.PetHealth.pet_id,
            "pet_name": record.pet_name,
            "pet_type": record.pet_type,
            "pet_status": record.pet_status,
            "owner_name": record.owner_name,
            "vaccinated": record.PetHealth.vaccinated,
            "spayed_neutered": record.PetHealth.spayed_neutered,
            "health_details": record.PetHealth.health_details,
            "good_with": {
                "children": record.PetHealth.good_with_children,
                "dogs": record.PetHealth.good_with_dogs,
                "cats": record.PetHealth.good_with_cats,
                "elderly": record.PetHealth.good_with_elderly,
                "strangers": record.PetHealth.good_with_strangers
            },
            "energy_level": record.PetHealth.energy_level,
            "temperament_personality": record.PetHealth.temperament_personality,
            "reason_for_adoption": record.PetHealth.reason_for_adoption,
            "created_at": record.PetHealth.created_at.isoformat(),
            "updated_at": record.PetHealth.updated_at.isoformat() if record.PetHealth.updated_at else None
        } for record in health_records]
    }

@router.get("/adoption-forms")
async def get_adoption_forms(
    status: str = Query(None, description="Filter by status: pending, approved, declined"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    # Base query with join to get user information
    query = db.query(
        models.AdoptionForm,
        models.User.name.label("user_name"),
        models.User.email.label("user_email")
    ).join(
        models.User, models.AdoptionForm.user_id == models.User.id
    ).order_by(
        models.AdoptionForm.created_at.desc()
    )

    # Apply status filter if provided
    if status:
        query = query.filter(models.AdoptionForm.status == status)

    # Apply search filter if provided
    if search:
        query = query.filter(
            or_(
                models.AdoptionForm.full_name.ilike(f"%{search}%"),
                models.User.name.ilike(f"%{search}%"),
                models.User.email.ilike(f"%{search}%")
            )
        )

    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    forms = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "status": status,
        "data": [{
            "id": form.AdoptionForm.id,
            "user_id": form.AdoptionForm.user_id,
            "user_name": form.user_name,
            "user_email": form.user_email,
            "status": form.AdoptionForm.status,
            "created_at": form.AdoptionForm.created_at.isoformat(),
            "applicant_info": {
                "full_name": form.AdoptionForm.full_name,
                "contact_info": form.AdoptionForm.contact_info,
                "housing_type": form.AdoptionForm.housing_type,
                "landlord_allows_pets": form.AdoptionForm.landlord_allows_pets
            },
            "household_details": {
                "members": form.AdoptionForm.household_members,
                "pet_allergies": form.AdoptionForm.pet_allergies,
                "allergy_types": form.AdoptionForm.allergy_types
            },
            "pet_care_plan": {
                "primary_caregiver": form.AdoptionForm.primary_caregiver,
                "expense_responsibility": form.AdoptionForm.expense_responsibility,
                "daily_alone_time": form.AdoptionForm.daily_alone_time,
                "alone_time_plan": form.AdoptionForm.alone_time_plan,
                "emergency_care": form.AdoptionForm.emergency_care
            },
            "pet_experience": {
                "current_pets": form.AdoptionForm.current_pets,
                "past_pets": form.AdoptionForm.past_pets,
                "past_pets_outcome": form.AdoptionForm.past_pets_outcome
            },
            "adoption_readiness": {
                "reason": form.AdoptionForm.adoption_reason,
                "household_agreement": form.AdoptionForm.household_agreement,
                "disagreement_reason": form.AdoptionForm.household_disagreement_reason
            }
        } for form in forms]
    }


@router.post("/announcements")
async def create_announcement(
    title: str = Body(..., embed=True),
    message: str = Body(..., embed=True),
    send_as_notification: bool = Body(True),
    db: Session = Depends(get_db)
):
    """
    Create a platform-wide announcement with duplicate prevention
    """
    if not title or not message:
        raise HTTPException(status_code=400, detail="Title and message are required")
    
    try:
        # Begin transaction
        db.begin()

        # More strict duplicate check (same title + message within last 30 minutes)
        duplicate_check = db.query(models.UserNotification)\
            .filter(
                models.UserNotification.title == f"Announcement: {title}",
                models.UserNotification.message == message[:500],
                models.UserNotification.created_at >= datetime.utcnow() - timedelta(minutes=30)
            )\
            .first()
        
        if duplicate_check:
            db.rollback()
            return {
                "success": False,
                "message": "Duplicate announcement prevented - identical message sent recently",
                "users_notified": 0
            }

        users = []
        if send_as_notification:
            # Get only active users
            users = db.query(models.User)\
                .filter(models.User.is_active == True)\
                .all()
            
            if not users:
                db.rollback()
                raise HTTPException(status_code=404, detail="No active users found")

            # Create all notifications at once
            notifications = [
                models.UserNotification(
                    user_id=user.id,
                    title=f"Announcement: {title}",
                    message=message[:500],
                    notification_type="system",
                    related_url="/announcements",
                    is_read=False,
                    created_at=datetime.utcnow()  # Explicit timestamp
                )
                for user in users
            ]
            
            # Bulk insert with explicit commit
            db.bulk_save_objects(notifications)
            db.commit()
        
        return {
            "success": True,
            "message": f"Announcement created{' and notifications sent' if send_as_notification else ''}",
            "users_notified": len(users) if send_as_notification else 0
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/announcements/unique")
async def get_unique_announcements(
    days: int = Query(7, description="Number of days to look back", gt=0, le=30),
    limit: int = Query(20, description="Maximum number of results", gt=0, le=100),
    db: Session = Depends(get_db)
):
    """
    Get unique system announcements (distinct by title/message)
    """
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get distinct announcements by title and message
        announcements = db.query(
            models.UserNotification.title,
            models.UserNotification.message,
            models.UserNotification.related_url,
            func.max(models.UserNotification.created_at).label("latest_date")
        )\
        .filter(
            models.UserNotification.notification_type == "system",
            models.UserNotification.created_at >= cutoff_date
        )\
        .group_by(
            models.UserNotification.title,
            models.UserNotification.message,
            models.UserNotification.related_url
        )\
        .order_by(desc("latest_date"))\
        .limit(limit)\
        .all()
        
        return [
            {
                "title": a.title,
                "message": a.message,
                "created_at": a.latest_date.isoformat(),
                "related_url": a.related_url
            }
            for a in announcements
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.patch("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    action: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if action == "suspend":
        user.is_active = False
        user.account_status = "suspended"
        user.deactivated_at = datetime.utcnow()
    elif action == "ban":
        user.is_active = False
        user.account_status = "banned"
        user.deactivated_at = datetime.utcnow()
    elif action == "reinstate":
        user.is_active = True
        user.account_status = "active"
        user.deactivated_at = None
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    db.commit()
    return {"success": True}


@router.get("/security/logs")
async def get_login_logs(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    user_id: Optional[int] = Query(None),
    email: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    attempt_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.LoginLog)
    
    # Apply filters
    if user_id:
        query = query.filter(models.LoginLog.user_id == user_id)
    if email:
        query = query.filter(models.LoginLog.email.ilike(f"%{email}%"))
    if status:
        query = query.filter(models.LoginLog.status == status)
    if attempt_type:
        query = query.filter(models.LoginLog.attempt_type == attempt_type)
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    logs = query.order_by(models.LoginLog.created_at.desc())\
               .offset((page - 1) * limit)\
               .limit(limit)\
               .all()
    
    return {
        "data": logs,
        "total": total,
        "page": page,
        "limit": limit
    }

