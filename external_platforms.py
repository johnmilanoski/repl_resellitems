import requests
from abc import ABC, abstractmethod

class ExternalPlatform(ABC):
    @abstractmethod
    def post_listing(self, listing):
        pass

class OfferUpPlatform(ExternalPlatform):
    def post_listing(self, listing):
        # TODO: Implement OfferUp API integration
        pass

class FacebookMarketplacePlatform(ExternalPlatform):
    def post_listing(self, listing):
        # TODO: Implement Facebook Marketplace API integration
        pass

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
