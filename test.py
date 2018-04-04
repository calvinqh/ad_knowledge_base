from adkb import ADKnowledgeBase
from configs import DBConfig as c

if __name__ == '__main__':
    kb = ADKnowledgeBase(c.getMongoConfig(), c.getCassandraConfig(), c.getNeo4JConfig())

    p_id = 'X690_120604'
    e_id = 'SLC27A4'
    t = 17    
    print(kb.getPatientReport(p_id))
    print()
    print(kb.getGeneReport(e_id))
    print()
    print(kb.find_name('17'))
    #print(kb.getNOrderGenes(t))
    print()
    print(kb.find_name('2'))
    print()
    print(kb.find_name('2391'))
    print()
    print(kb.find_name('987'))
    print()
    print(kb.find_name('23647'))

