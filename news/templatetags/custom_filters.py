from django import template


register = template.Library()

'''@register.filter(name='Censor')
def Censor(text):
    matfur = text
    replica = 'Censor'
    mathst = ['it', 'cпорт']
    mathf = matfur.replace(' ', ' ').lower().split(' ')

    for i in range(len(mathf)):
        if mathf[i] in mathst:
            mathf[i] = ''.join('Censor')
    resault = ' '.join(mathf)
    return resault'''


@register.filter(name='Censor')
def censor(text):
    matfur = text
    mathst = ['it', 'cпорт']
    mathf = matfur.replace(' ', ' ').lower().split(' ')

    for ot in mathf:
        if ot in mathst:
            i = ''.join('Censor')
            mathf = [x.replace(ot, i) for x in mathf]
    resault = ' '.join(mathf)
    return resault
