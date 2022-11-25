lis1=['once upon a time','A long time ago','A few years ago']
list2=["there was lived a boy named rounak","there was lived a young man","there was lived a old man "]
list3=["he was very happy ","he was very delighted","he alawys make a people happy"]
list4=["he alawys believe in god","he never give up in any situation","he alawys believe in her family"]
list5=["he helped many people ","he encourage many people","he alaways help poor people"]
list6=["without any ego ","with a kind heart","with a positive mindset"]
c="Are you interested in story ? \nIf yes then please enter 'yes' other wise 'no' "
print(c)
import random
def story(list):
    a=(random.choice(list))
    return a
def story2(list2):
    b=(random.choice(list2))
    return b
def story3(list3):
    c=random.choice(list3)
    return c
def story4(list4):
    d=random.choice(list4)
    return d
def story5(list5):
    e=random.choice(list5)
    return e
def story6(list6):
    f=random.choice(list6)
    return f
int=input()

if int=="yes":
    k=input("Enter your name:")
    print("welcome",k)
    print(story(lis1)+","+story2(list2)+ " " +story3(list3)+" "+story5(list5)+" "+story(list6))


elif int=="no":
    print("It's Ok that you don't want any story\nProgram ended.... ")

else:
    print("Invalid input")

