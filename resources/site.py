from flask_restful import Resource
from models.site import SiteModel

class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):

    def get(self, url):
        site = SiteModel.find_site(url)
        if not site:
            return {'message': 'site not found'},404
        return site.json()

    def post(self, url):
        if SiteModel.find_site(url):
            return {'message': f'The site {url} already existis'}, 400 
    
        site = SiteModel(url)
         
        try:
            site.save_site()
        except:
            return {'message': 'An internal error has ocurred'}, 500     
        return site.json()

    def delete(self, url):
        site = SiteModel.find_site(url)    
        if not site:
            return {'message': 'Site not found'}
        try:    
            site.delete_site()    
        except:
            {'message': 'An internal error has ocurred'}, 500     
        return {'message': 'Site deleted'}