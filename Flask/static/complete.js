document.addEventListener('DOMContentLoaded', () => {
  const encodeProgress = document.getElementById('encodeProgress');
  const saveButton = document.getElementById('saveCapture');
  const closeButton = document.getElementById('close');
  const review = document.getElementById('review');
  const status = document.getElementById('status');
  let format;
  let audioURL;
  let encoding = false;
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if(request.type === "createTab") {
      format = request.format;
      let startID = request.startID;
      status.innerHTML = "Please wait..."
      closeButton.onclick = () => {
        chrome.runtime.sendMessage({cancelEncodeID: startID});
        chrome.tabs.getCurrent((tab) => {
          chrome.tabs.remove(tab.id);
        });
      }

      //if the encoding completed before the page has loaded
      if(request.audioURL) {
        encodeProgress.style.width = '100%';
        status.innerHTML = "File is ready!"
        generateSave(request.audioURL);
      } else {
        encoding = true;
      }
    }

    //when encoding completes
    if(request.type === "encodingComplete" && encoding) {
      encoding = false;
      status.innerHTML = "File is ready!";
      encodeProgress.style.width = '100%';
      generateSave(request.audioURL);
    }
    //updates encoding process bar upon messages
    if(request.type === "encodingProgress" && encoding) {
      encodeProgress.style.width = `${request.progress * 100}%`;
    }
    function generateSave(url) { //creates the save button
      const currentDate = new Date(Date.now()).toDateString();
      saveButton.onclick = () => {
		  var audio = new Audio(url);
      chrome.downloads.download({url: url, filename: "notes.wav", saveAs: true});
      console.log(url);
      var req =  fetch('http://localhost:5000/audio/', {
        method: 'post',
        body: "text"
      })
      var text;
      req.then(response=>response.text()).then(result=> {text=result})
      var req = new XMLHttpRequest();
      req.open("POST", "http://localhost:5000/downloadfile/" + text , true);
      req.responseType = "blob";
      req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      req.onreadystatechange = function(){
      if (this.readyState == 4 && this.status == 200){
          var blob = new Blob([this.response], {type: "application/pdf"});
          var url = window.URL.createObjectURL(blob);
          var link = document.createElement('a');
          document.body.appendChild(link);
          link.style = "display: none";
          link.href = url;
          link.download = "minutes_of_meeting.pdf";
          link.click();

          setTimeout(() => {
          window.URL.revokeObjectURL(url);
          link.remove(); } , 100);
      }
      };
      req.send();
      };
      saveButton.style.display = "inline-block";
    }
  });
  review.onclick = () => {
    chrome.tabs.create({url: "https://chrome.google.com/webstore/detail/chrome-audio-capture/kfokdmfpdnokpmpbjhjbcabgligoelgp/reviews"});
  }


})
