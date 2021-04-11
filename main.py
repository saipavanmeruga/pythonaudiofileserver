from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# Init app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audio.db'

db = SQLAlchemy(app)

# Here we use SQLAlchemy ORM
# Song Class/Model


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class Song(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Song_name = db.Column(db.String(100), nullable=False)
    Song_duration = db.Column(db.Integer, nullable=False)
    Song_uploadedtime = db.Column(db.DateTime, nullable=False)

    def __init__(self, ID, Name, Duration, UploadedTime):
        self.ID = ID
        self.Song_name = Name
        self.Song_duration = Duration
        self.Song_uploadedtime = UploadedTime

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.ID,
            'Song_name': self.Song_name,
            'Song_duration': self.Song_duration,
            'Song_uploadedtime': dump_datetime(self.Song_uploadedtime),
        }


class Podcast(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Podcast_name = db.Column(db.String(100), nullable=False)
    Podcast_duration = db.Column(db.Integer, nullable=False)
    Podcast_uploadedtime = db.Column(db.DateTime, nullable=False)
    Podcast_host = db.Column(db.String(100), nullable=False)
    Podcast_participants = db.Column(db.String(500), nullable=True)

    def __init__(self, ID, Name, Duration, Uploaded_time, Host, Participants):
        self.ID = ID
        self.Podcast_name = Name
        self.Podcast_duration = Duration
        self.Podcast_uploadedtime = Uploaded_time
        self.Podcast_host = Host
        self.Podcast_participants = Participants

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.ID,
            'Podcast_name': self.Podcast_name,
            'Podcast_duration': self.Podcast_duration,
            'Podcast_uploadedtime': dump_datetime(self.Podcast_uploadedtime),
            'Podcast_host': self.Podcast_host,
            'Podcast_participants': self.Podcast_participants
        }


class Audiobook(db.Model):

    ID = db.Column(db.Integer, primary_key=True)
    Audiobook_title = db.Column(db.String(100), nullable=False)
    Audiobook_author = db.Column(db.String(100), nullable=False)
    Audiobook_narrator = db.Column(db.String(100), nullable=False)
    Audiobook_duration = db.Column(db.Integer, nullable=False)
    Audiobook_uploadedtime = db.Column(db.DateTime, nullable=False)

    def __init__(self, ID, Title, Author, Narrator, Duration, Uploaded_time):
        self.ID = ID
        self.Audiobook_title = Title
        self.Audiobook_author = Author
        self.Audiobook_narrator = Narrator
        self.Audiobook_duration = Duration
        self.Audiobook_uploadedtime = Uploaded_time

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.ID,
            'Audiobook_title': self.Audiobook_title,
            'Audiobook_duration': self.Audiobook_duration,
            'Audiobook_uploadedtime': dump_datetime(self.Audiobook_uploadedtime),
            'Audiobook_narrator': self.Audiobook_narrator,
            'Audiobook_author': self.Audiobook_author
        }


# Create a audioFileType
db.create_all()


@app.route('/create', methods=['POST'])
def createAPI():
    try:
        audioFileType = request.json['audioFileType']
        audioFileMetadata = request.json['audioFileMetadata']
        if audioFileType == "song":   # ID	Name	Duration	Uploaded_time
            audioFileMetadata['Uploaded_time'] = datetime.now()
            newSong = Song(audioFileMetadata["ID"], audioFileMetadata["Name"],
                           audioFileMetadata["Duration"], audioFileMetadata["Uploaded_time"])
            db.session.add(newSong)
            db.session.commit()
            return jsonify({"Created song audiofile": "200 OK"}), 200
        elif audioFileType == "podcast":  # ID	Name	Duration	Uploaded_time	Host	Participants
            audioFileMetadata['Uploaded_time'] = datetime.now()
            newPodcast = Podcast(audioFileMetadata["ID"], audioFileMetadata["Name"], audioFileMetadata["Duration"],
                                 audioFileMetadata["Uploaded_time"], audioFileMetadata["Host"], audioFileMetadata["Participants"])

            db.session.add(newPodcast)
            db.session.commit()
            return jsonify({"Created podcast audiofile": "200 OK"}), 200
        elif audioFileType == "audiobook":  # ID	Title	Author	Narrator	Duration	Uploaded_time
            audioFileMetadata["Uploaded_time"] = datetime.now()
            newAudiobook = Audiobook(audioFileMetadata["ID"], audioFileMetadata["Title"], audioFileMetadata["Author"],
                                     audioFileMetadata["Narrator"], audioFileMetadata["Duration"], audioFileMetadata["Uploaded_time"])
            db.session.add(newAudiobook)
            db.session.commit()
            return jsonify({"Created audiobook audiofile": "200 OK"}), 200
        else:
            return jsonify({"The request is invalid": " 400 bad request"}), 400
    except Exception as e:
        print(e)
        return jsonify({"Any error": "500 internal server error"}), 500


@app.route('/<string:audioFileType>/<int:audioFileID>', methods=['DELETE'])
def deleteAPI(audioFileType, audioFileID):
    try:
        if audioFileType == "song":
            song = Song.query.get(audioFileID)
            db.session.delete(song)
            db.session.commit()
            return jsonify({"Deleted song": "200 OK"}), 200
        elif audioFileType == "podcast":
            podcast = Podcast.query.get(audioFileID)
            db.session.delete(podcast)
            db.session.commit()
            return jsonify({"Deleted Podcast": "200 OK"}), 200
        elif audioFileType == "audiobook":
            audiobook = Audiobook.query.get(audioFileID)
            db.session.delete(audiobook)
            db.session.commit()
            return jsonify({"Deleted Audiobook": "200 OK"}), 200

        else:
            return jsonify({"The request is invalid": " 400 bad request"}), 400
    except:
        return jsonify({"Any error": "500 internal server error"}), 500


@app.route('/<string:audioFileType>', methods=['GET'])
@app.route('/<string:audioFileType>/<int:audioFileID>', methods=['GET'])
def readAPI(audioFileType, audioFileID=0):
    try:
        if audioFileType == "song":
            if audioFileID == 0:
                all_songs = Song.query.all()
                return jsonify(json_list=[i.serialize for i in all_songs])
            else:
                song = Song.query.get(audioFileID)
                return jsonify(song.serialize)

        elif audioFileType == "podcast":
            if audioFileID == 0:
                all_podcast = Podcast.query.all()
                return jsonify(json_list=[i.serialize for i in all_podcast])
            else:
                podcast = Podcast.query.get(audioFileID)
                return jsonify(podcast.serialize)
        elif audioFileType == "audiobook":
            if audioFileID == 0:
                all_audiobook = Audiobook.query.all()
                return jsonify(json_list=[i.serialize for i in all_audiobook])
            else:
                audiobook = Audiobook.query.get(audioFileID)
                return jsonify(audiobook.serialize)
        else:
            return jsonify({"The request is invalid": " 400 bad request"}), 400
    except:
        return jsonify({"Any error": "500 internal server error"}), 500


@app.route('/<string:audioFileType>/<int:audioFileID>', methods=['PUT'])
def updateAPI(audioFileType, audioFileID):
    try:
        audioFileMetadata = request.json['audioFileMetadata']
        if audioFileType == "song":
            song = Song.query.get(audioFileID)

            song.ID = audioFileMetadata["ID"]
            song.Song_name = audioFileMetadata["Name"]
            song.Song_duration = audioFileMetadata["Duration"]
            song.Song_uploadedtime = datetime.now()
            db.session.commit()
            return jsonify({"Updated song details": "200 OK"}), 200
        elif audioFileType == "podcast":
            podcast = Podcast.query.get(audioFileID)
            podcast.Podcast_name = audioFileMetadata["Name"]
            podcast.Podcast_duration = audioFileMetadata["Duration"]
            podcast.Podcast_uploadedtime = audioFileMetadata["Uploaded_time"]
            podcast.Podcast_host = audioFileMetadata["Host"]
            podcast.Podcast_participants = audioFileMetadata["Participants"]
            db.session.commit()
            return jsonify({"Updated podcast details": "200 OK"}), 200

        elif audioFileType == "audiobook":
            audiobook = Audiobook.query.get(audioFileID)
            audiobook.ID = audioFileMetadata["ID"]
            audiobook.Audiobook_title = audioFileMetadata["Title"]
            audiobook.Audiobook_author = audioFileMetadata["Author"]
            audiobook.Audiobook_narrator = audioFileMetadata["Narrator"]
            audiobook.Audiooook_duration = audioFileMetadata["Duration"]
            audiobook.Audiobook_uploadedtime = audioFileMetadata["Uploaded_time"]
            db.session.commit()
            return jsonify({"Updated audiobook ddetails": "200 OK"}), 200
        else:
            return jsonify({"The request is invalid": " 400 bad request"}), 400
    except Exception as e:
        print(e)
        return jsonify({"Any error": "500 internal server error"}), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello World!'


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
