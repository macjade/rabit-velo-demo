$(document).ready(function() {
    var qrcode = window.qrcode;

    const video = document.createElement("video");
    const canvasElement = document.getElementById("qr-canvas");
    const canvas = canvasElement.getContext("2d");

    const qrResult = document.getElementById("qr-result");
    const outputData = document.getElementById("outputData");
    const btnScanQR = document.getElementById("btn-scan-qr");

    let scanning = false;

    function generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r:(r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    qrcode.callback = (res) => {
      if (res) {
        outputData.innerText = res;
        scanning = false;

        video.srcObject.getTracks().forEach(track => {
          track.stop();
        });

        $.ajax({
            url: '/scanner/scanned/'+res.replaceAll('/', '__')+'/',
            type: 'GET',
            success: function(e) {
                if (e.status) {
                    window.location = e.url;
                }else {
                    M.toast({html: e.message, classes: ' red lighten-2 white-text'});
                    startscan();
                }
            }
        })
      }
    };

    //btnScanQR.onclick = () =>{
    function startscan() {
        navigator.mediaDevices
            .getUserMedia({ video: { facingMode: "environment" } })
            .then(function(stream) {
              scanning = true;
              qrResult.hidden = true;
              btnScanQR.hidden = true;
              canvasElement.hidden = false;
              video.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
              video.srcObject = stream;
              video.play();
              tick();
              scan();
            });
    }

    startscan();

    //};

    function tick() {
      canvasElement.height = video.videoHeight;
      canvasElement.width = video.videoWidth;
      canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);

      scanning && requestAnimationFrame(tick);
    }

    function scan() {
      try {
        qrcode.decode();
      } catch (e) {
        setTimeout(scan, 300);
      }
    }
});