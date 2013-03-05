from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from Products.Archetypes.ArchetypeTool import registerType
from Products.CMFCore.utils import getToolByName
from bika.lims.browser.bika_listing import BikaListingView
from bika.health.config import PROJECTNAME, GENDERS_APPLY
from bika.lims import bikaMessageFactory as _b
from bika.health import bikaMessageFactory as _
from bika.lims.content.bikaschema import BikaFolderSchema
from bika.health.interfaces import ISymptoms
from plone.app.layout.globals.interfaces import IViewView
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.folder.folder import ATFolder,ATFolderSchema
from zope.interface.declarations import implements
from operator import itemgetter

class SymptomsView(BikaListingView):
    implements(IFolderContentsView,IViewView)

    def __init__(self,context,request):
        super(SymptomsView,self).__init__(context,request)
        self.catalog='bika_setup_catalog'
        self.contentFilter={'portal_type': 'Symptom',
                              'sort_on': 'sortable_title'}
        self.context_actions={_('Add'):
                                {'url': 'createObject?type_name=Symptom',
                                 'icon': '++resource++bika.lims.images/add.png'}}
        self.title=_("Symptoms")
        self.icon = self.portal_url + "/++resource++bika.health.images/symptom_big.png"
        self.description=_("Additional Symptoms not covered by ICD codes, can be entered here.")
        self.show_sort_column=False
        self.show_select_row=False
        self.show_select_column=True
        self.pagesize=25

        self.columns={
            'Title': {'title': _('Symptom'),
                      'index':'sortable_title'},
            'Description': {'title': _('Description'),
                            'index': 'description',
                            'toggle': True},
            'Gender': {'title': _('Gender'),
                            'index': 'gender',
                            'toggle': True},
        }

        self.review_states=[
            {'id':'default',
             'title': _('Active'),
             'contentFilter': {'inactive_state': 'active'},
             'transitions': [{'id':'deactivate'},],
             'columns': ['Title',
                         'Description',
                         'Gender']},
            {'id':'inactive',
             'title': _('Dormant'),
             'contentFilter': {'inactive_state': 'inactive'},
             'transitions': [{'id':'activate'},],
             'columns': ['Title',
                         'Description',
                         'Gender']},
            {'id':'all',
             'title': _('All'),
             'contentFilter':{},
             'columns': ['Title',
                         'Description',
                         'Gender']},
        ]

    def folderitems(self):
        items=BikaListingView.folderitems(self)
        for x in range(len(items)):
            if not items[x].has_key('obj'): continue
            obj=items[x]['obj']
            items[x]['Description']=obj.Description()
            items[x]['Gender']=GENDERS_APPLY.getValue(obj.getGender())
            items[x]['replace']['Title']="<a href='%s'>%s</a>"%\
                 (items[x]['url'],items[x]['Title'])

        return items

schema=ATFolderSchema.copy()
class Symptoms(ATFolder):
    implements(ISymptoms)
    displayContentsTab=False
    schema=schema

schemata.finalizeATCTSchema(schema,folderish=True,moveDiscussion=False)
atapi.registerType(Symptoms,PROJECTNAME)
