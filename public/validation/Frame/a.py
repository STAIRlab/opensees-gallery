

class ForceElement:
    layout = const

    def getTangent(self):
        self.section: Section

        self.section.getTangentChild(self.layout)
#       k = self.getTangent()
#       k[..] += ...
#       return k[layout, layout]





class Section:
    def getTangentParent(layout):
        k = self.getTangent()
        if len(layout) == 6:
            k[..] += ...
        return k[layout, layout]

    def getFlexibilityParent(layout):
        f = self.getFlexibility()
        return f[layout, layout]



    def getTangentChild():
        pass

    def getFlexibilityChild():
        pass



class ElasticSection(Section):
    def __init__(self):
        self.k = [...]
        self.f = inv(self.k)
        self.f6 = inv(self.k[:6,:6])

    def setTrialStrain(self, e):
        self.e = e

    def getFlexibility(layout):
        return self.f

        if len(layout) == 6:
            return self.f6
        else:
            return self.f




class FiberSection(Section):

    def __init__(self):
        ...


    def setTrialStrain(self, e):
        self.e = e



    def getTangent():
        return sum(
                f(self.e)...
        )

    def getFlexibility(layout):
        return inv(self.getTangent(layout))


section = Section()

