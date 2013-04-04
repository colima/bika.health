from bika.lims.browser.sample import SamplesView
from Products.CMFCore.utils import getToolByName


class SamplesView(SamplesView):

    def __init__(self, context, request):
        super(SamplesView, self).__init__(context, request)

    def contentsMethod(self, contentFilter):
        tool = getToolByName(self.context, self.catalog)
        state = [x for x in self.review_states if x['id'] == self.review_state][0]
        for k, v in state['contentFilter'].items():
            self.contentFilter[k] = v
        tool_samples = tool(contentFilter)
        samples = {}
        for sample in (p.getObject() for p in tool_samples):
            for ar in sample.getAnalysisRequests():
                if ar['Patient'] == self.context.UID():
                    samples[sample.getId()] = sample
        return samples.values()
