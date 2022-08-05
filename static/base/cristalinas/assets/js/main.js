jQuery(function($) {
    "use strict";
    /*Table OF Contents
	==========================
	1-Custome Placeholder
	2-Home slider
	3-Parallax
	4-custome selectbox
	5-Twitter
	6-Owl slider
	7-Masonry
	8-Show Trending Song List
	9-Events countdown
	10-Date Time Picker
	11-Audio Player for blog post
	12-Player for Individual Songs
	13-packery
	14-Google Maps
	15-Menu
	16-Header Player
	17-WavePlayer ( used in header)
    */

    /*==========================
    ajax call
    ========================
    var xv_ww = $(window).width(),
        xv_slideshow = true;
    
    $('#ajaxArea').ajaxify({forms: false,requestDelay:500});
    
	$(window).on('pronto.render', function(event, eventInfo){
        $('html, body').animate({scrollTop: 0});
		suonoApp();
		$('.pageLoader').removeClass("active");
	});
	
    $(window).on('pronto.request', function(event, eventInfo){
		$('.pageLoader').addClass("active");
	});*/
    
    
        /*==============================================
        Song List
        ==============================================*/
        $("body").on("click", ".showAllTrending", function(e) {
            var $this = $(this);
            e.preventDefault();
            $this.fadeOut();
            $(".populateSongList li").show();
            $("body,html").animate({
                scrollTop: $(".populateSongList").offset().top - 70
            });
        });

        /*================
        Events countdown
        ====================*/
        if ($('.countdown').length) {
            $('.countdown').each(function(num, ele) {
                var $this = $(this);
                $this.downCount({
                    date: '09/09/2016 12:00:00',
                    offset: +10
                }, function() {
                    alert('WOOT WOOT, done!');
                });
            });
        }

        /*================
        date time picker
        ====================*/
        if ($('.xvDatePicker').length) {
            $(".xvDatePicker").each(function(num, ele) {
                var $this = $(this);
                $this.datetimepicker({
                    timepicker: false
                });
            });
        }

        /*=========================
        Audio Player for blog post
        =========================*/
        if ($(".post-audio-player").length) {
            $('.post-jplayer').each(function(num, ele) {
                var temp_id = $(this).attr("id"),
                    temp_song = $(this).attr('data-mp3'),
                    temp_title = $(this).attr('data-title'),
                    temp_wrap = "#" + $(this).parents(".post-audio-player").attr("id");
                $(".post-jplayer#" + temp_id).jPlayer({
                    play: function() {
                        $(this).jPlayer("pauseOthers"); // pause all players except this one.
                    },
                    ready: function() {
                        $(this).jPlayer("setMedia", {
                            mp3: temp_song,
                            title: temp_title
                        });
                    },
                    cssSelectorAncestor: temp_wrap,
                    volume: 0.5,
                    supplied: "mp3",
                    swfPath: "assets/js/jPlayer/jquery.jplayer.swf",
                });
            });
        }

        /*============================
        Player for Individual Songs
        ==============================*/

        if ($(".singleSongPlayer").length) {
            $('.singleSong-jplayer').each(function(num, ele) {
                var temp_id = $(this).attr("id"),
                    temp_song = $(this).attr('data-mp3'),
                    temp_title = $(this).attr('data-title'),
                    temp_wrap = "#" + $(this).parents(".singleSongPlayer").attr("id");
                $(".singleSong-jplayer#" + temp_id).jPlayer({
                    play: function() {
                        $(this).jPlayer("pauseOthers"); // pause all players except this one.
                    },
                    ready: function() {
                        $(this).jPlayer("setMedia", {
                            mp3: temp_song,
                            title: temp_title
                        });
                    },
                    cssSelectorAncestor: temp_wrap,
                    volume: 0.5,
                    supplied: "mp3",
                    swfPath: "assets/js/jPlayer/jquery.jplayer.swf",
                });
            });
        }

        /*=======================================
        packery
        =======================================*/
        if ($('.xvPackeryItems').length) {
            var packery = $('.xvPackeryItems');
            packery.packery({
                itemSelector: '.xvPackeryItem',
                gutter: 0
            });
        }
        

        
        /*===========================
        Contact
        ============================
        function IsEmail(email) {
			var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
			return regex.test(email);
		}
		
		if($("#contactForm").length!=0){
			$("#contactForm").submit(function (e) {
				e.preventDefault();
				var name = $("#xv_name").val(),
				email = $("#xv_email").val(),
				message = $("#xv_message").val(),
				dataString = 'name=' + name + '&email=' + email + '&message=' + message;
		
				if (name === '' || !IsEmail(email) || message === '') {  
                    $(".validationError").show();
				} else {
					$.ajax({
						type: "POST",
						url: "assets/php/submit.php",
						data: dataString,
						success: function () {
							$('#contactForm').slideUp();
							$(".messageSentSuccess").fadeIn();
						}
					});
				}
				return false;
			});
		}*/
           



    /*==============================================
	Header Player
	==============================================*/

    $('body').on("click", function(e) {
        if (!$(e.target).closest('.the-xv-Jplayer').length) {
            $(".jp-playlist").slideUp();
            $("body").removeClass("playerFullOn");
        }
    });

    $(".sound-trigger").click(function(e) {
        $(this).parent(".jp-volume-controls").toggleClass("open");
    });

    $(".playList-trigger").click(function(e) {
        $("body").toggleClass("playerFullOn");
        $(".jp-playlist").slideToggle();
    });

    var werock;

    if ($('#audio-player').length) {
        $("#player-instance").jPlayer({
            cssSelectorAncestor: "#audio-player",
        });

        if ($('.playlist-files').length) {
            var playlist_items = [],
                $playlist_audio = $('.playlist-files li'),
                playlist_items_length = $playlist_audio.length;
            for (var i = 0; i < playlist_items_length; i++) {
                var new_playlist_item = {};
                new_playlist_item['title'] = $playlist_audio.eq(i).attr('data-title');
                new_playlist_item['artist'] = $playlist_audio.eq(i).attr('data-artist');
                new_playlist_item['mp3'] = $playlist_audio.eq(i).attr('data-mp3');
                playlist_items.push(new_playlist_item);
            }

            werock = new jPlayerPlaylist({
                jPlayer: "#player-instance",
                enableRemoveControls: false,
                cssSelectorAncestor: "#audio-player"
            }, playlist_items, {
                playlistOptions: {
                    autoPlay: false,
                    loopOnPrevious: true
                }
            }, {
                swfPath: "assets/js/jPlayer/jquery.jplayer.swf",
                supplied: "mp3",
                displayTime: 'fast',
                addTime: 'fast',
            });


            $("#player-instance").bind($.jPlayer.event.play, function(event) {
                var current = werock.current,
                    playlist = werock.playlist;
                jQuery.each(playlist, function(index, obj) {
                    if (index == current) {
                        $('.the-xv-Jplayer .audio-title').html('<span class="jp-artist">' + obj.artist + '</span><span class="jp-songTitle">' + obj.title + '</span>');
                    }
                });
            });
        }


        $('.jp-prev').click(function() {
            werock.previous();
        });
    }

    if ($('#audio-player-radio').length) {
        var streamUrl = $('#audio-player-radio').attr("data-radio-url"),
            radioName = $('#audio-player-radio').attr("data-title"),
            stream = {
                title: radioName,
                mp3: streamUrl
            },
            radio_ready = false;
        $("#player-instance-radio").jPlayer({
            ready: function(event) {
                radio_ready = true;
                $(this).jPlayer("setMedia", stream).jPlayer("pause");
            },
            pause: function() {
                $(this).jPlayer("clearMedia");
            },
            error: function(event) {
                if (radio_ready && event.jPlayer.error.type === $.jPlayer.error.URL_NOT_SET) {
                    $(this).jPlayer("setMedia", stream).jPlayer("play");
                }
            },
            cssSelectorAncestor: "#audio-player-radio",
            swfPath: "assets/js/jPlayer/jquery.jplayer.swf",
            preload: "none"
        });
    }

    /*================
    WavePlayer ( used in header)
    ====================*/
    var $wavePlayer = $(".waveSurferPlayer"),
        $wave = $("#waveform"),
        wavColor = $wave.attr("data-wave-color"),
        waveProgress = $wave.attr("data-wave-progress"),
        waveCursor = $wave.attr("data-cursor"),
        waveHeight = +$wave.attr("data-height");

    function onWaveSurferInitialized(wavesurfer) {
        wavesurfer = Object.create(WaveSurfer),
            wavesurfer.init({
                container: '#waveform',
                waveColor: wavColor,
                progressColor: waveProgress,
                cursorColor: waveCursor,
                height: waveHeight
            });
        wavesurfer.load('assets/demo-data/demo.wav');
        wavesurfer.on('ready', function(e) {
            wavesurfer.play();
            $(".playWave").hide();
        });
        wavesurfer.on('error', function(err) {
            console.error(err);
        });
        wavesurfer.on('finish', function() {
            console.log('Finished playing');
            $(".pauseWave").hide();
            $(".playWave").show();
        });
        $("body").on("click", ".playWave", function(e) {
            e.preventDefault();
            wavesurfer.play();
            $(this).hide();
            $(".pauseWave").show();
        });
        $("body").on("click", ".pauseWave", function(e) {
            e.preventDefault();
            wavesurfer.pause();
            $(this).hide();
            $(".playWave").show();
        });
        $("body").on("click", ".muteWave", function(e) {
            e.preventDefault();
            $(this).toggleClass("pc-mute", "pc-volume");
            wavesurfer.toggleMute();
        });
    } /*wave init funtion*/


    if ($wavePlayer.length) {
      	var waveSurfer;
        if (WaveSurfer.Swf.supportsAudioContext() && WaveSurfer.Swf.supportsCanvas()) {
            waveSurfer = Object.create(WaveSurfer);
            onWaveSurferInitialized(waveSurfer);
        } else {
            swfobject.embedSWF('assets/js/wavesurfer/wavesurfer.swf', 'wavesurfer', '100%', '128', '11.1.0', 'expressInstall.swf', {}, {
                allowScriptAccess: 'always'
            }, {});
            waveSurfer = new WaveSurfer.Swf();
            waveSurfer.on('init', function() {
                onWaveSurferInitialized(waveSurfer);
            });
        }
    }




});