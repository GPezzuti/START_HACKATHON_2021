let config = {
  headers: {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer BQAzNz64nkwLFnJDS5RimAn7VtwKDN-X5IYLaGUfh49vrbVkNu_QbXMaWDQIBUzQRu2mOyjEOzi-n-yLupU"
  }
}

const token = document.querySelector("#token").value;
console.log(token)
config.headers["Authorization"] = `Bearer ${token}`;

function csvJSON(csv){

  var lines=csv.split("\n");

  var result = [];

  // NOTE: If your columns contain commas in their values, you'll need
  // to deal with those before doing the next step 
  // (you might convert them to &&& or something, then covert them back later)
  // jsfiddle showing the issue https://jsfiddle.net/
  var headers=lines[0].split(",");

  for(var i=1;i<lines.length;i++){

      var obj = {};
      var currentline=lines[i].split(",");

      for(var j=0;j<headers.length;j++){
          obj[headers[j]] = currentline[j];
      }

      result.push(obj);

  }

  //return result; //JavaScript object
  return JSON.stringify(result); //JSON
}
const stringData = `id,album,name,artist,explicit,popularity,danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,type,uri,track_href,analysis_url,duration_ms,time_signature
1paoZeTSzzgjsxIATeRDO9,2pRX61FqphSRtenHWqkydF,Classroom,Yxngxr1,True,35,0.6774086159653361,0.40115881339217707,4,10.976225288756105,0,0.038657801903374006,0.4088679232715689,0.21195076898323603,0.0004735815524360004,0.26819002427972094,5.360810622244415,audio_features,spotify:track:1paoZeTSzzgjsxIATeRDO9,https://api.spotify.com/v1/tracks/1paoZeTSzzgjsxIATeRDO9,https://api.spotify.com/v1/audio-analysis/1paoZeTSzzgjsxIATeRDO9,0.9262179215273934,4
6wFqLYmiXyGvprbWa4ogm8,57KCk6H2jdmgHeh0JNW95b,i think too much,Christian French,False,65,0.4744086159653361,0.1941588133921771,7,15.018225288756105,0,0.12304219809662598,0.6010379232715689,0.21192126898323604,0.0004735815524360004,0.26219002427972105,5.327810622244414,audio_features,spotify:track:6wFqLYmiXyGvprbWa4ogm8,https://api.spotify.com/v1/tracks/6wFqLYmiXyGvprbWa4ogm8,https://api.spotify.com/v1/audio-analysis/6wFqLYmiXyGvprbWa4ogm8,0.02483458819406037,4
2ZyReDZVgl6cZomz8MEyvv,0zC4qbIE37BG6b8kKu9UA6,GIRL IN YELLOW,Yxngxr1,True,44,0.612408615965336,0.36215881339217704,10,13.183225288756104,1,0.0013421980966259739,0.2348679232715689,0.21192616898323602,0.071773581552436,0.0008099757202789659,48.74018937775557,audio_features,spotify:track:2ZyReDZVgl6cZomz8MEyvv,https://api.spotify.com/v1/tracks/2ZyReDZVgl6cZomz8MEyvv,https://api.spotify.com/v1/audio-analysis/2ZyReDZVgl6cZomz8MEyvv,1.2127012548607268,4
17tDv8WA8IhqE8qzuQn707,1W9toxqtPfieKk6cft0f7R,My First Kiss (feat. Ke$ha),"3OH!3, Kesha",False,64,0.48140861596533613,0.00015881339217704848,0,18.711225288756104,1,0.11794219809662598,0.5992279232715689,0.21195076898323603,0.296773581552436,0.4271900242797211,40.668189377755596,audio_features,spotify:track:17tDv8WA8IhqE8qzuQn707,https://api.spotify.com/v1/tracks/17tDv8WA8IhqE8qzuQn707,https://api.spotify.com/v1/audio-analysis/17tDv8WA8IhqE8qzuQn707,0.19715125486072704,4
41jZtFqmBlC0maxnobrQtv,0canh94jv3jOqOh7n8L1z2,I Don't Need A Reason,Dizzee Rascal,True,43,0.363408615965336,0.15715881339217708,1,18.338225288756107,1,0.03965780190337401,0.5463679232715689,0.21195076898323603,0.0007735815524359951,0.10919002427972102,72.59718937775557,audio_features,spotify:track:41jZtFqmBlC0maxnobrQtv,https://api.spotify.com/v1/tracks/41jZtFqmBlC0maxnobrQtv,https://api.spotify.com/v1/audio-analysis/41jZtFqmBlC0maxnobrQtv,0.109817921527394,4
2nUy0ifVE7UwtOK4rugFsP,6NrMjaGIZAKZLMzVnkNY4V,The End of Heartache,Killswitch Engage,False,62,0.26840861596533605,0.08684118660782292,0,19.308225288756105,0,0.08734219809662598,0.6045809232715689,0.0050492310167639665,0.00037358155243599755,0.17780997572027898,26.648189377755585,audio_features,spotify:track:2nUy0ifVE7UwtOK4rugFsP,https://api.spotify.com/v1/tracks/2nUy0ifVE7UwtOK4rugFsP,https://api.spotify.com/v1/audio-analysis/2nUy0ifVE7UwtOK4rugFsP,1.5639654118059396,4
`;
let parsedCsv = JSON.parse(csvJSON(stringData));
console.log(parsedCsv)
let albumAndTrackIds = parsedCsv.map(sD => (sD.album && sD.id 
  ? { albumId: sD.album, trackId: sD.id, album: sD.name } 
  : false))
albumAndTrackIds = albumAndTrackIds.filter(Boolean);
const tracksOfAlbum = [];
let currentAlbumIdx = 0;
let currentTrack;
let currentTrackUrl;
let errorCounter = 0;

const song = document.querySelector("#song");
const songSource = document.querySelector("#song-source");
const playlist = document.querySelector("#playlist");

albumAndTrackIds.forEach(sD => {
  const li = document.createElement('li');
  li.textContent = sD.album;
  playlist.appendChild(li);
})

function getAlbum() {
  return fetch(`https://api.spotify.com/v1/albums/${albumAndTrackIds[currentAlbumIdx].albumId}`, {
    headers: config.headers
  })
}

function getTrack() {
  currentTrack = tracksOfAlbum.find(t => t.id === albumAndTrackIds[currentAlbumIdx].trackId)
  currentTrackUrl = currentTrack.preview_url;
  if (currentTrackUrl) {
    playlist.childNodes[currentAlbumIdx].classList.add("active")
    songSource.src = currentTrackUrl;
    song.load();
    song.play();
  } else {
    alert('No demo for this track')
    currentAlbumIdx++;
    if (currentAlbumIdx === albumAndTrackIds.length) {
      currentAlbumIdx = 0;
    }
    init();
  }
}

song.onended = function() {
  playlist.childNodes[currentAlbumIdx].classList.remove("active")
  currentAlbumIdx++;
  if (currentAlbumIdx === albumAndTrackIds.length) {
    currentAlbumIdx = 0;
  }
  init();
}

let hasTracks = false;

function init() {
  getAlbum()
    .then(res => res.json())
    .then(res => {
      tracksOfAlbum.push(...res.tracks.items) 
      if (!hasTracks) {
        hasTracks = true;
        playlist.childNodes.forEach((node, i) => {
          node.textContent += ` - ${tracksOfAlbum[i].name}`
        })
      }
      getTrack()
    })
    .catch(err => {
      errorCounter++;
      currentAlbumIdx = 0;
      if (errorCounter < 5) {
        init();
      }
    })
}

init();