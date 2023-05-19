import xml.sax
import csv


thedatawriter=None


class PostsHandler(xml.sax.ContentHandler):
    def startElement(self, name, attrs):
        if name == "row":
            postType=int(attrs["PostTypeId"])
            if postType <=2:
                
                ownerDisplayName=''
                ownerId=""
                user=""
                if "OwnerUserId" in attrs:
                    ownerId=attrs["OwnerUserId"]
                    user=ownerId
                    if ownerId in userIdsToNames:
                        ownerDisplayName=userIdsToNames[ownerId]
                        user=ownerDisplayName +' ('+ownerId+')'
                elif "OwnerDisplayName" in attrs:
                    ownerDisplayName=attrs["OwnerDisplayName"]
                    user = ownerDisplayName
                tags =[]
                if "Tags" in attrs:
                    tags=re.split("[<>]+", attrs["Tags"])
                    tags = [x for x in tags if len(x)>0]

                csvTags=""
                for tag in tags:
                    if len(csvTags)>0:
                        csvTags+=","
                    csvTags+=tag
                questionId = attrs["Id"]
                if postType ==2:
                    
                    questionId = attrs["ParentId"]


                creationDate=None
                title=None
                acceptedAnswerId=None
                answerId=None
                if postType ==1:
                    if "CreationDate" in attrs:
                        creationDate=attrs["CreationDate"]
                    if "Title" in attrs:
                        title = attrs["Title"]
                    if "AcceptedAnswerId" in attrs:
                        acceptedAnswerId = attrs["AcceptedAnswerId"]
                if postType ==2:
                    if "CreationDate" in attrs:
                        creationDate=attrs["CreationDate"]
                    if "Id" in attrs:
                        answerId=attrs["Id"]
                if title is not None:
	                title.replace("\n"," ").replace("\r"," ")

                row=[questionId,answerId,csvTags,user,creationDate,acceptedAnswerId,title]
                thedatawriter.writerow(row)



userIdsToNames={}
class UsersHandler(xml.sax.ContentHandler):
    def startElement(self, name, attrs):
        if name == "row":
            userIdsToNames[attrs["Id"]] = attrs["DisplayName"]


parser = xml.sax.make_parser()


print ("loading Users")
parser.setContentHandler(UsersHandler())
parser.parse(open("Users.xml", "r"))

print ("loading Posts")
postsFilename="Posts.xml"
with open('posts.csv', 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile)
    parser.setContentHandler(PostsHandler())
    parser.parse(open(postsFilename, "r"))
