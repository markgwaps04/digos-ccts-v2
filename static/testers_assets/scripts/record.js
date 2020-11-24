(function (jq) {

    let recorder;
    let context;
    let audioButton = document.querySelector('.js-record');
    let $audioButton = $(audioButton);
    let audioMediaElement = jq("audio.audio_src");
    let tracks;
    const $playButton = jq(".js-play");
    const $input_audio = jq("input[name='audio_blob']");
    let ready_update = false;

    if (audioMediaElement.length) {
        $playButton.removeClass("button--disabled");
        audioMediaElement = audioMediaElement[0];
        ready_update = true;


        // fetch("http://127.0.0.1:8000/media/audio_base/b434e7b2-5201-47e0-b760-d2224a1139e7.mp3")
        //     .then(response => response.blob())
        //     .then(function (response) {
        //          const url = window.URL.createObjectURL(response);
        //          console.log(url);
        //     });
    }


    window.test = audioMediaElement;


    window.URL = window.URL || window.webkitURL;
    /**
     * Detecte the correct AudioContext for the browser
     * */

    window.AudioContext = window.AudioContext || window.webkitAudioContext;
    navigator.getUserMedia = navigator.getUserMedia
        || navigator.webkitGetUserMedia
        || navigator.mozGetUserMedia
        || navigator.msGetUserMedia;

    const stopPlay = function () {

        $playButton
            .removeClass("button--active")
            .find("i")
            .removeClass("fa-stop")
            .addClass("fa-play");

        audioMediaElement.pause();
        audioMediaElement.currentTime = 0;
        $audioButton.removeClass("button--disabled");

        $playButton
            .off("click")
            .on("click", playRecord);

    }

    const playRecord = function () {

        $playButton.trigger("on_play_record");

        $playButton
            .addClass("button--active")
            .find("i")
            .removeClass("fa-play")
            .addClass("fa-stop");

        audioMediaElement.play();
        $audioButton.addClass("button--disabled");

        $playButton
            .off("click")
            .on("click", stopPlay);

        audioMediaElement.addEventListener('ended', function () {
            stopPlay();
        });

    }

    const onFail = function (e) {
        alert('Error ' + e);
        console.log('Rejected!', e);

        $audioButton
            .removeClass("button--active")
            .find("i")
            .removeClass("fa-stop")
            .addClass("fa-microphone");

        $audioButton
            .off("click")
            .on("click", startRecord);

        $playButton.removeClass("button--disabled");

    };

    const stopRecord = function () {

        setTimeout(function () {

            recorder.stop();
            tracks.forEach(track => track.stop());
            recorder.exportWAV(function (s) {

                window.define_value("record_audio", s);

                const url = window.URL.createObjectURL(s);
                var au = document.createElement('audio');
                //add controls to the <audio> element
                console.log(s);
                au.src = url;
                $input_audio.val(url);

                audioMediaElement = au;
                $playButton.removeClass("button--disabled");

                $audioButton
                    .off("click")
                    .on("click", startRecord);

            });

        }, 1000);

        $audioButton
            .removeClass("button--active")
            .find("i")
            .removeClass("fa-stop")
            .addClass("fa-microphone");


    }

    const onSuccess = function (s) {

        tracks = s.getTracks();
        context = new AudioContext();
        let mediaStreamSource = context.createMediaStreamSource(s);
        recorder = new Recorder(mediaStreamSource);
        recorder.record();

        $audioButton
            .addClass("button--active")
            .find("i")
            .removeClass("fa-microphone")
            .addClass("fa-stop");

        $audioButton
            .off("click")
            .on("click", stopRecord);

        $playButton.addClass("button--disabled");

    }

    const startRecord = function () {
        if (navigator.getUserMedia) {
            /**
             * ask permission of the user for use microphone or camera
             */
            navigator.getUserMedia({audio: true}, onSuccess, onFail);
        } else {
            console.warn('navigator.getUserMedia not present');
        }
    }

    $audioButton.on("click", startRecord);
    $playButton.on("click", playRecord);

})(jQuery)
