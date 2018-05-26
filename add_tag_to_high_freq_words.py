import sys, os

# Load Anki library
sys.path.append(os.path.join(os.getcwd(),"anki"))
from anki.storage import Collection

# Define the path to the Anki SQLite collection
PROFILE_HOME = os.path.expanduser("/home/hermuba/.local/share/Anki2/User 1")
cpath = os.path.join(PROFILE_HOME, "collection.anki2")

# Load the Collection
col = Collection(cpath, log=True) # Entry point to the API

# Use the available methods to list the notes
high_freq = []
for cid in col.findNotes("tag:high-frequency-words"):
    note = col.getNote(cid)
    front =  note.fields[0] # "Front" is the first field of these cards
    high_freq.append(front)

# find all in Barron 3500
for cid in col.findNotes("Deck:Barron3500"):
    note = col.getNote(cid)
    word = note.fields[0].split('[')[0].replace(' ','').replace('&nbsp', '').replace(';', '')
    if word in high_freq:
        note.tags = col.tags.canonify(col.tags.split("high-freq-350"))

        m = note.model()
        m['tags'] = note.tags

        col.models.save(m)
        col.addNote(note)
        print(note.fields[0])
        high_freq.remove(word)
col.save()
