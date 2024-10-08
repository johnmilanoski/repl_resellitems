import requests
from abc import ABC, abstractmethod
from models import Notification, db
from flask import current_app

class ExternalPlatform(ABC):
    @abstractmethod
    def post_listing(self, listing):
        pass

    @abstractmethod
    def check_comments(self, listing):
        pass

class OfferUpPlatform(ExternalPlatform):
    def post_listing(self, listing):
        # TODO: Implement OfferUp API integration
        pass

    def check_comments(self, listing):
        # TODO: Implement OfferUp API integration to check for new comments
        # For now, we'll simulate a new comment
        new_comment = {
            'content': 'Is this item still available?',
            'platform': 'OfferUp'
        }
        self._create_notification(listing, new_comment)

class FacebookMarketplacePlatform(ExternalPlatform):
    def post_listing(self, listing):
        # TODO: Implement Facebook Marketplace API integration
        pass

    def check_comments(self, listing):
        # TODO: Implement Facebook Marketplace API integration to check for new comments
        # For now, we'll simulate a new comment
        new_comment = {
            'content': 'Can you provide more details about the condition?',
            'platform': 'Facebook Marketplace'
        }
        self._create_notification(listing, new_comment)

    def _create_notification(self, listing, comment):
        notification = Notification(
            user_id=listing.user_id,
            listing_id=listing.id,
            content=comment['content'],
            platform=comment['platform']
        )
        db.session.add(notification)
        db.session.commit()

def post_to_external_platforms(listing):
    platforms = [
        OfferUpPlatform(),
        FacebookMarketplacePlatform(),
    ]
    
    results = []
    for platform in platforms:
        try:
            result = platform.post_listing(listing)
            results.append({"platform": platform.__class__.__name__, "success": True, "result": result})
        except Exception as e:
            results.append({"platform": platform.__class__.__name__, "success": False, "error": str(e)})
    
    return results

def check_external_platforms_comments(listing):
    platforms = [
        OfferUpPlatform(),
        FacebookMarketplacePlatform(),
    ]
    
    for platform in platforms:
        try:
            platform.check_comments(listing)
        except Exception as e:
            current_app.logger.error(f"Error checking comments on {platform.__class__.__name__}: {str(e)}")
