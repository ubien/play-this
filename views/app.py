import cgi
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache
from mako.template import Template
from mako.runtime import Context
import simplejson
import md5
import urllib
import logging

LOG_FILENAME = '/Users/Jacob/projects/playthis/play-this/demoque.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)




API_URL = 'http://1.apishark.com/p:y3p001'

class Song:
    def __init__(self,id,song,artist):
        self.id = id
        self.name = song
        self.artist = artist
        self.album = 'album'
        self.votes =  '0'
    def jsonify(self):
        response = {"SongID" : self.id,
                "SongName" : self.name,
                "ArtistName" : self.artist,
                "AlbumName" : self.album,
                "votes" : self.votes };
        return response

def jsonifySongs(songs):
    s = len(songs) - 1
    i = 0
    result = '{'
    for song in songs:
        result += '"'+str(i)+'"' + ' : ' + str(Song.jsonify(song))
        if i<s :
            result += ', '
        
        i += 1
    
    result += '}'
    return result;

def gsAuth():
    url = API_URL + '/genGSAuth/'
    username = 'ubien'
    pw = 'kflip402'
    token = md5.new(username + md5.new(pw).hexdigest()).hexdigest()
    params = urllib.urlencode({'username': username, 'token': token})
    f = urllib.urlopen(url, params)
    #auth_resp = f.read()
    result = simplejson.load(f)
    token = -1
    if result['Success'] == True:
        token = result['Result']
    return token

def getPlaylistID(gsauth,playlistName):
    url = API_URL + '/getUserPlaylistsEx/'
    type = "gsauth"
    data = gsauth
    url += type + '/' + data
    f = urllib.urlopen(url)
    result = simplejson.load(f)
    if result['Success'] == False:
        return -1
    pl_id = -1
    result_list = result['Result']
    for i in range(0,len(result_list)):
        if result_list[i]['Name'].find(playlistName) != -1:
            pl_id = result_list[i]['PlaylistID']
    return result_list
    if pl_id == -1:
        return -2
    return pl_id

def getPlaylistSongs(playlist_id):
    url = API_URL + '/getPlaylistInfo/'
    url += playlist_id
    f = urllib.urlopen(url)
    result = simplejson.load(f)
    if result['Success'] == False:
        return -1
    return result['Result']['Songs']

def addSong(gsauth,playlist_id,song_id):

    
class Home(webapp.RequestHandler):
    def get(self):
        logging.debug('This message should go to the log file')
        mytemplate = Template(filename='../templates/index.html')
        songs = []
        songs.append(Song('1','fuck you','ceelo green'))
        songs.append(Song('2','good vibrations','beach boys'))
        songs.append(Song('3','hot like sauce','Pretty Lights'))
        token = memcache.get("token")
        if token is None:
            token=gsAuth()
        if token == -1:
            print mytemplate.render(error="omg login no worky")
        else:
            memcache.add("token", token, 1000)
            #playlist_id = getPlaylistID(token,"play-this")
            playlist_id = '51284718'
            if (playlist_id == -2):
                print mytemplate.render(error='cant find playlist:play-this')
            else:
                playlist_songs = getPlaylistSongs(playlist_id)
                if playlist_songs == -1:
                    print mytemplate.render(error='get songs for playlist'+str(playlist_id))

            print mytemplate.render(songs=jsonifySongs(songs), playlist=playlist_songs)

    
class VoteAction(webapp.RequestHandler):
    def post(self):
        results = self.request.get('SongID')
        self.response.out.write(results)


class SearchSongs(webapp.RequestHandler):
    def post(self):
        query = self.request.get('search')
        query_url = ' /searchSongs/'
        result = '{"Success":true,"Result":[{"SongID":27392819,"SongName":"Finally Moving","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":28631733,"SongName":"Happiness (Troubled Faces)","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":27392824,"SongName":"The Last Passenger","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":837090,"SongName":"Blue Lights","ArtistID":4975,"ArtistName":"Pretty Girls Make Graves","AlbumID":132555,"AlbumName":"The New Romance","CoverArtFilename":"c51c67735d3d717509485a803225e384.png","IsVerified":true},{"SongID":22957032,"SongName":"Pretty Dancer","ArtistID":2252,"ArtistName":"Mos Def","AlbumID":2945380,"AlbumName":"The Ecstatic","CoverArtFilename":"2945380.jpg","IsVerified":true},{"SongID":19192036,"SongName":"Love Like Honey","ArtistID":319,"ArtistName":"Pretty Ricky","AlbumID":2736020,"AlbumName":"Late Night Special","CoverArtFilename":"2481439.jpg","IsVerified":true},{"SongID":13988948,"SongName":"Up and Down","ArtistID":319,"ArtistName":"Pretty Ricky","AlbumID":2736020,"AlbumName":"Late Night Special","CoverArtFilename":"2481439.jpg","IsVerified":true},{"SongID":23206355,"SongName":"Lights Out","ArtistID":659,"ArtistName":"Breaking Benjamin","AlbumID":3431993,"AlbumName":"Dear Agony","CoverArtFilename":"3431993.jpg","IsVerified":true},{"SongID":16623677,"SongName":"Theme for a Pretty Girl That Makes You Believe God Exists","ArtistID":2002,"ArtistName":"Eels","AlbumID":2515870,"AlbumName":"Blinking Lights and Other Revelations (disc 1)","CoverArtFilename":"4854489.jpg","IsVerified":true},{"SongID":23294012,"SongName":"Can\'t Stop Me Now","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":3525674,"AlbumName":"Passing By Behind Your Eyes","CoverArtFilename":"3525674.jpg","IsVerified":false},{"SongID":24677496,"SongName":"I Can See It In Your Face","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":4030451,"AlbumName":"Making Up A Changing Mind","CoverArtFilename":"4030451.jpg","IsVerified":false},{"SongID":23294309,"SongName":"Keep Em Bouncin","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":3525674,"AlbumName":"Passing By Behind Your Eyes","CoverArtFilename":"3525674.jpg","IsVerified":false},{"SongID":23526574,"SongName":"Sunday School","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":3525674,"AlbumName":"Passing By Behind Your Eyes","CoverArtFilename":"3525674.jpg","IsVerified":false},{"SongID":24677810,"SongName":"Total Fascination","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":4030451,"AlbumName":"Making Up A Changing Mind","CoverArtFilename":"4030451.jpg","IsVerified":false},{"SongID":20829683,"SongName":"Out of Control","ArtistID":609026,"ArtistName":"Capital Lights","AlbumID":2857885,"AlbumName":"This Is an Outrage!","CoverArtFilename":"2857885.jpg","IsVerified":true},{"SongID":20829685,"SongName":"Miracle Man","ArtistID":609026,"ArtistName":"Capital Lights","AlbumID":2857885,"AlbumName":"This Is an Outrage!","CoverArtFilename":"2857885.jpg","IsVerified":true},{"SongID":24677661,"SongName":"Understand Me Now","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":4030451,"AlbumName":"Making Up A Changing Mind","CoverArtFilename":"4030451.jpg","IsVerified":false},{"SongID":24677924,"SongName":"Still Rockin","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":4030451,"AlbumName":"Making Up A Changing Mind","CoverArtFilename":"4030451.jpg","IsVerified":false},{"SongID":24677321,"SongName":"Easy Way Out","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":4030451,"AlbumName":"Making Up A Changing Mind","CoverArtFilename":"4030451.jpg","IsVerified":false},{"SongID":24677200,"SongName":"Future Blind","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":4030451,"AlbumName":"Making Up A Changing Mind","CoverArtFilename":"4030451.jpg","IsVerified":false},{"SongID":20829681,"SongName":"Outrage","ArtistID":609026,"ArtistName":"Capital Lights","AlbumID":2857885,"AlbumName":"This Is an Outrage!","CoverArtFilename":"2857885.jpg","IsVerified":true},{"SongID":23294138,"SongName":"World Of Illusion","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":3525674,"AlbumName":"Passing By Behind Your Eyes","CoverArtFilename":"3525674.jpg","IsVerified":false},{"SongID":23294231,"SongName":"If I Could Feel Again","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":3525674,"AlbumName":"Passing By Behind Your Eyes","CoverArtFilename":"3525674.jpg","IsVerified":false},{"SongID":23294301,"SongName":"City Of One","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":3525674,"AlbumName":"Passing By Behind Your Eyes","CoverArtFilename":"3525674.jpg","IsVerified":false},{"SongID":419171,"SongName":"Pretty Girls Make Graves","ArtistID":3729,"ArtistName":"The Smiths","AlbumID":184803,"AlbumName":"The Smiths","CoverArtFilename":"2ef58a7f547f33631230f48af01a91e0.png","IsVerified":true},{"SongID":23524700,"SongName":"Dark As The Sky","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":3525674,"AlbumName":"Passing By Behind Your Eyes","CoverArtFilename":"3525674.jpg","IsVerified":false},{"SongID":23294154,"SongName":"Let Em Know It\'s Time To Go","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":3525674,"AlbumName":"Passing By Behind Your Eyes","CoverArtFilename":"3525674.jpg","IsVerified":false},{"SongID":23293992,"SongName":"Short Cut\/Detour","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":3525674,"AlbumName":"Passing By Behind Your Eyes","CoverArtFilename":"3525674.jpg","IsVerified":false},{"SongID":23294245,"SongName":"Someday Is Everyday","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":3525674,"AlbumName":"Passing By Behind Your Eyes","CoverArtFilename":"3525674.jpg","IsVerified":false},{"SongID":23293973,"SongName":"Lonesome Street","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":3525674,"AlbumName":"Passing By Behind Your Eyes","CoverArtFilename":"3525674.jpg","IsVerified":false},{"SongID":3167738,"SongName":"Who You Talkin\' To?","ArtistID":19634,"ArtistName":"Sloan","AlbumID":339754,"AlbumName":"Pretty Together","CoverArtFilename":"d3c196544a9e902140ba17a89c7b680e.png","IsVerified":true},{"SongID":7320083,"SongName":"P.Y.T. (Pretty Young Thing)","ArtistID":39,"ArtistName":"Michael Jackson","AlbumID":126163,"AlbumName":"Thriller","CoverArtFilename":"5edc8010370a5247607ac5dbdbde1a01.png","IsVerified":true},{"SongID":211457,"SongName":"It Must Look Pretty Appealing","ArtistID":812,"ArtistName":"Bad Religion","AlbumID":191787,"AlbumName":"No Control","CoverArtFilename":"155fe04d80232925bdd9a5fd606842c0.png","IsVerified":true},{"SongID":9142750,"SongName":"Pretty Picture of a Broken Face","ArtistID":29145,"ArtistName":"Hot Cross","AlbumID":222498,"AlbumName":"Cryonics","CoverArtFilename":"2993488.jpg","IsVerified":true},{"SongID":8733674,"SongName":"Turn the Lights Out When You Leave","ArtistID":8,"ArtistName":"Elton John","AlbumID":199694,"AlbumName":"Peachtree Road","CoverArtFilename":"199694.png","IsVerified":true},{"SongID":837097,"SongName":"A Certain Cemetery","ArtistID":4975,"ArtistName":"Pretty Girls Make Graves","AlbumID":132555,"AlbumName":"The New Romance","CoverArtFilename":"c51c67735d3d717509485a803225e384.png","IsVerified":true},{"SongID":23294192,"SongName":"Ask Your Friends","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":3525674,"AlbumName":"Passing By Behind Your Eyes","CoverArtFilename":"3525674.jpg","IsVerified":false},{"SongID":21456586,"SongName":"04Finally Moving","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":21456583,"SongName":"01Short Line","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":21456595,"SongName":"13Almost Familiar","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":21456585,"SongName":"03Wrong Platform ","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":21456584,"SongName":"02Until Tomorrow","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":21456588,"SongName":"06Summer\'s Thirst","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":21456592,"SongName":"10Samso","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":21456587,"SongName":"05Stay","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":21456594,"SongName":"12Happiness (Troubled Faces)","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":21456597,"SongName":"15Try To Remember","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":21456591,"SongName":"09Waiting For Her","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":21456593,"SongName":"11Down The Line","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false},{"SongID":21456596,"SongName":"14The Last Passenger","ArtistID":1041960,"ArtistName":"Pretty Lights","AlbumID":2954041,"AlbumName":"Taking Up Your Precious Time","CoverArtFilename":"2954041.jpg","IsVerified":false}],"ServerID":1,"RateLimit":{"CallsRemaining":195,"ResetTime":1301508808,"CallsMade":4,"RemainingSecs":3479,"CacheBusts":0},"Cache":{"FromCache":false,"CacheBusted":false}}'
        self.response.out.write(result)

        
application = webapp.WSGIApplication(
                                     [('/', Home),
                                      ('/playthis', VoteAction),
                                     ('/searchthis', SearchSongs)],
                                     debug=True)
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()