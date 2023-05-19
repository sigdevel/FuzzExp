



from itertools import groupby
from unicodedata import decomposition, name
from pprint import pprint as pp

commonleaders = ['the'] 
replacements = {u'ß': 'ss',  
                u'ſ': 's',
                u'ʒ': 's',
                }

hexdigits = set('0123456789abcdef')
decdigits = set('0123456789')   

def splitchar(c):
    ' De-ligature. De-accent a char'
    de = decomposition(c)
    if de:
        
        de = [d for d in de.split()
                  if all(c.lower()
                         in hexdigits for c in d)]
        n = name(c, c).upper()
        
        if len(de)> 1 and 'PRECEDE' in n:
            
            de[1], de[0] = de[0], de[1]
        tmp = [ unichr(int(k, 16)) for k in de]
        base, others = tmp[0], tmp[1:]
        if 'LIGATURE' in n:
            
            base += others.pop(0)
    else:
        base = c
    return base


def sortkeygen(s):
    '''Generate 'natural' sort key for s

    Doctests:
        >>> sortkeygen('  some extra    spaces  ')
        [u'some extra spaces']
        >>> sortkeygen('CasE InseNsItIve')
        [u'case insensitive']
        >>> sortkeygen('The Wind in the Willows')
        [u'wind in the willows']
        >>> sortkeygen(u'\462 ligature')
        [u'ij ligature']
        >>> sortkeygen(u'\335\375 upper/lower case Y with acute accent')
        [u'yy upper/lower case y with acute accent']
        >>> sortkeygen('foo9.txt')
        [u'foo', 9, u'.txt']
        >>> sortkeygen('x9y99')
        [u'x', 9, u'y', 99]
    '''
    
    s = unicode(s).strip()
    
    s = ' '.join(s.split())
    
    s = s.lower()
    
    words = s.split()
    if len(words) > 1 and words[0] in commonleaders:
        s = ' '.join( words[1:])
    
    s = ''.join(splitchar(c) for c in s)
    
    s = ''.join( replacements.get(ch, ch) for ch in s )
    
    s = [ int("".join(g)) if isinteger else "".join(g)
          for isinteger,g in groupby(s, lambda x: x in decdigits)]

    return s

def naturalsort(items):
    ''' Naturally sort a series of strings

    Doctests:
        >>> naturalsort(['The Wind in the Willows','The 40th step more',
                         'The 39 steps', 'Wanda'])
        ['The 39 steps', 'The 40th step more', 'Wanda', 'The Wind in the Willows']

    '''
    return sorted(items, key=sortkeygen)

if __name__ == '__main__':
    import string

    ns = naturalsort

    print '\n
    txt = ['%signore leading spaces: 2%+i' % (' '*i, i-2) for i in range(4)]
    print 'Text strings:'; pp(txt)
    print 'Normally sorted :'; pp(sorted(txt))
    print 'Naturally sorted:'; pp(ns(txt))

    print '\n
    txt = ['ignore m.a.s%s spaces: 2%+i' % (' '*i, i-2) for i in range(4)]
    print 'Text strings:'; pp(txt)
    print 'Normally sorted :'; pp(sorted(txt))
    print 'Naturally sorted:'; pp(ns(txt))

    print '\n
    txt = ['Equiv.%sspaces: 3%+i' % (ch, i-3)
           for i,ch in enumerate(reversed(string.whitespace))]
    print 'Text strings:'; pp(txt)
    print 'Normally sorted :'; pp(sorted(txt))
    print 'Naturally sorted:'; pp(ns(txt))

    print '\n
    s = 'CASE INDEPENENT'
    txt = [s[:i].lower() + s[i:] + ': 3%+i' % (i-3) for i in range(1,5)]
    print 'Text strings:'; pp(txt)
    print 'Normally sorted :'; pp(sorted(txt))
    print 'Naturally sorted:'; pp(ns(txt))

    print '\n
    txt = ['foo100bar99baz0.txt', 'foo100bar10baz0.txt',
           'foo1000bar99baz10.txt', 'foo1000bar99baz9.txt']
    print 'Text strings:'; pp(txt)
    print 'Normally sorted :'; pp(sorted(txt))
    print 'Naturally sorted:'; pp(ns(txt))

    print '\n
    txt = ['The Wind in the Willows','The 40th step more',
                         'The 39 steps', 'Wanda']
    print 'Text strings:'; pp(txt)
    print 'Normally sorted :'; pp(sorted(txt))
    print 'Naturally sorted:'; pp(ns(txt))

    print '\n
    txt = ['Equiv. %s accents: 2%+i' % (ch, i-2)
           for i,ch in enumerate(u'\xfd\xddyY')]
    print 'Text strings:'; pp(txt)
    print 'Normally sorted :'; pp(sorted(txt))
    print 'Naturally sorted:'; pp(ns(txt))

    print '\n
    txt = [u'\462 ligatured ij', 'no ligature',]
    print 'Text strings:'; pp(txt)
    print 'Normally sorted :'; pp(sorted(txt))
    print 'Naturally sorted:'; pp(ns(txt))

    print '\n
    s = u'ʒſßs' 
    txt = ['Start with an %s: 2%+i' % (ch, i-2)
           for i,ch in enumerate(s)]
    print 'Text strings:'; pp(txt)
    print 'Normally sorted :'; print '\n'.join(sorted(txt))
    print 'Naturally sorted:'; print '\n'.join(ns(txt))
