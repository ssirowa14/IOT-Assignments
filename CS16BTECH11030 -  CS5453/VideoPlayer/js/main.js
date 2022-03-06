/*
 * Refereces:
 * https://github.com/SamsungDForum/PlayerHTML5/tree/master/PlayerHTML5
 * https://github.com/Samsung/TizenTVApps/tree/master/TVDemoVideoPlayer
 */

(function(){

    var player = null;
    var videos = ["video/sample0.mp4", "video/sample1.mp4", "video/sample2.mp4"];
    var source = 0;

    //catch Input from Remote
    function catchFromRemote() {
        document.addEventListener('keydown', function (e) {
            switch (e.keyCode) {
            
                case 37:	//left
                	console.log("REWINDING 10s");
                	player.currentTime = Math.max(0, player.currentTime-10);
                    break;

                case 39:	//right
                	console.log("FORWARDING 10s");
                	player.currentTime = Math.min(player.duration, player.currentTime+10);
                    break;
                    
                case 38:	//up
                	source = (source+1)%3;
                	player.src = videos[source];             
                	player.load();
                	player.pause();
                	player.currentTime = 0;         
                	console.log("Video source changed");
                    break;
                
                case 40:	//down
                	source = (source-1+3)%3;
                	player.src = videos[source];             
                	player.load();
                	player.pause();
                	player.currentTime = 0;
                	console.log("Video source changed");
                	break;
                	
                case 447:	//volume down
                	player.volume = Math.max(0.0, player.volume-0.1);
                	console.log("Volume: "+player.volume);
                	break;
                	
                case 448:	//volume up
                	player.volume = Math.min(1.0, player.volume+0.1);
                	console.log("Volume: "+player.volume);
                	break;

                case 13:	//ok
                	if(player.paused === true){
                		console.log("VIDEO PLAYED");
                		player.play();
                	}
                	else{
                		console.log("VIDEO PAUSED");
                		player.pause();
                	}
                	break;

                default:
                	console.log("UNRECOGNISED KEY: " + e.keyCode);
                    break;
            }
        });
    }
    
    function formatTime(seconds){
    	var hh = Math.floor(seconds / 3600), mm = Math.floor(seconds / 60) % 60, ss = Math.floor(seconds) % 60;	  
    	return (hh ? (hh < 10 ? "0" : "") + hh + ":" : "") + ((mm < 10) ? "0" : "") + mm + ":" + ((ss < 10) ? "0" : "") + ss;
    }
    
    //update progress bar
    function startProgressBar(){
    	player.addEventListener('timeupdate', function(){
    		var duration = player.duration;
    		document.getElementById('progress-amount').style.width = ((player.currentTime / duration)*100) + "%";
	    	document.getElementById("current-time").innerHTML = formatTime(player.currentTime);
	    	document.getElementById("total-time").innerHTML = formatTime(player.duration);
    	}, false);
    }

    //called after document unloaded
    function onUnload() {
    	console.log('onUnload');
        player.pause();
    }

    //called as soon as document loaded
    window.onload = function () {
        player = document.getElementById("videoTag");
        document.getElementById("total-time").innerHTML = formatTime(player.duration);
        catchFromRemote();
        startProgressBar();
        document.body.addEventListener('unload', onUnload);      
    };
})();