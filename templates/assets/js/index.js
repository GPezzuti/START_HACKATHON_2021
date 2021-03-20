let config = {
  headers: {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer BQAzNz64nkwLFnJDS5RimAn7VtwKDN-X5IYLaGUfh49vrbVkNu_QbXMaWDQIBUzQRu2mOyjEOzi-n-yLupU"
  }
}

const token = document.querySelector("#token").value;
config.headers["Authorization"] = `Bearer ${token}`;
let csv;

fetch("http://localhost:5000/getPlotCSV").then(res => res.text()).then(res => {
  csv = res;

  let parsedCsv = JSON.parse(csvJSON(csv));
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
})

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