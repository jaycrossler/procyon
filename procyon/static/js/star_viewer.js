var star_viewer = {};

star_viewer.is_rendered = false;
star_viewer.particles = [];
star_viewer.lastClicked = null;
star_viewer.lastColor = null;
star_viewer.highlightLine = null;
star_viewer.show_sun = false;
star_viewer.stars_to_show = 4;
star_viewer.star_scale_default = .005;
star_viewer.central_sun = null;
star_viewer.bounds = 60;
star_viewer.close_by_boundary = 0.5;
star_viewer.initial_stars_shown = 50;
star_viewer.zoom_throttle = 5;
star_viewer.zoom_close_throttle = 15;
star_viewer.zoom_out_throttle = 5;
star_viewer.zoom_out_max = 120;
star_viewer.star_canvas_size = 96;
star_viewer.mass_rescale = 20;
star_viewer.camera_movement_speed = 1;
star_viewer.camera_look_speed = 0.005;
star_viewer.function_run_when_close = function(){
    console.log("Close");
};
star_viewer.PI2 = Math.PI * 2;

var program = function ( context, color ) {
    context.fillStyle = color.__styleString;
    context.beginPath();
    context.arc( 0, 0, 1, 0, star_viewer.PI2, true );
    context.closePath();
    context.fill();
};

star_viewer.preloader=function() {
    star_viewer.init(); //Set up the star_viewer.scene and star_viewer.renderer
    star_viewer.animate(); //Start updating the star_viewer.scene as often as possible
};

star_viewer.init=function() {
    star_viewer.container = document.getElementById( 'container'  );
    star_viewer.div_details =document.getElementById( 'details' );
    star_viewer.div_info= document.getElementById( 'info' );
    star_viewer.scene = new THREE.Scene();
    star_viewer.init_central_sun();
    star_viewer.init_camera();
    star_viewer.init_grid();
    star_viewer.init_renderer();
    star_viewer.init_stats();

    star_viewer.init_object_points(false,false,true);
};
star_viewer.init_central_sun=function(){
    for ( var i = 0; i <= stars.length; i ++ ) {
        var star = stars[i];
        if (star && star.centered) {
            star_viewer.central_sun = star;
            break;
        }
    }

};
//=======================================
star_viewer.generateSunTexture=function(color, size, showShell, altColor) {
    var size = (size) ? parseInt(size*star_viewer.star_canvas_size) : star_viewer.star_canvas_size;
    var showShell = (showShell) ? showShell : false;
    var canvas = document.createElement( 'canvas' );
    canvas.width = size;
    canvas.height = size;
    var col = new THREE.Color(color);

    var context = canvas.getContext( '2d' );
    var gradient = context.createRadialGradient( canvas.width / 2, canvas.height / 2, 0, canvas.width / 2, canvas.height / 2, canvas.width / 2 );
    gradient.addColorStop( 0, col.rgbaString);
    gradient.addColorStop( 0.1, col.rgbaString);
    gradient.addColorStop( 0.7, altColor || col.rgbaPrefixString + '0.2)');//'rgba(125, 20, 0, 0.2)' );
    gradient.addColorStop( 0.8, 'rgba(125, 20, 0, 0.3)' );
    if (showShell) {
        gradient.addColorStop( 0.85, 'rgba(0, 20, 0, 1)' );
        gradient.addColorStop( 0.9, 'rgba(255, 255, 255, 0.2)' );
    }
    gradient.addColorStop( .98, 'rgba(0,0,0,0)' );
    context.fillStyle = gradient;
    context.fillRect( 0, 0, canvas.width, canvas.height );
    return canvas;
};
star_viewer.init_object_points=function(show_amount, isRedder, isHideDwarfs) {

    show_amount = show_amount || star_viewer.initial_stars_shown || stars.length;
    var color_offset = (isRedder) ? 0x006050 : 0x000000;

    //currently, the star_viewer.particles are rendered differently
    if (star_viewer.option_RenderEngine == "webgl") {
        if (star_viewer.is_rendered) {
            //delete everything
            star_viewer.scene.removeObject(star_viewer.particles);
            star_viewer.is_rendered = false;
        }

        //Staring sun
        var geometry = new THREE.Geometry();
// 					var vector = new THREE.Vertex( new THREE.Vector3( 0,0,0 ));
// 					vector.name = "Sol: The Sun";
// 					geometry.vertices.push( vector );
// 					geometry.colors[ 0 ] = new THREE.Color( 0xfff2a1 - color_offset );

        //Stars
        for ( var i = 0; i <= show_amount; i ++ ) {
            if (i >= stars.length) break;
            var obj = stars[i];
//            if (isHideDwarfs && (obj.starType.charAt(0) == "M")) continue; //Hide M-type stars
            vector = new THREE.Vertex(new THREE.Vector3( obj.x, obj.y, obj.z ));
            vector.name = obj.name;
            vector.starid = i;

            var color = parseInt(obj.web_color.replace("#",""), 16) - color_offset;
            vector.color = (color);

            geometry.vertices.push( vector );
            geometry.colors.push( new THREE.Color( obj.color - color_offset ) );
        }

        var sprite = ImageUtils.loadTexture( "textures/sprites/sun2.png" );
        var scale = star_viewer.star_scale_default;

        var material = new THREE.ParticleBasicMaterial( { size: scale, map: sprite, blending: THREE.AdditiveBlending, vertexColors: true } );

        star_viewer.particles = new THREE.star_viewer.particlesystem( geometry, material );
        star_viewer.particles.sortstar_viewer.particles = true;
        star_viewer.particles.isClickable = true;
        star_viewer.particles.updateMatrix();
        star_viewer.scene.addObject( star_viewer.particles );

    } else { //for Canvas and SVG
        if (star_viewer.is_rendered) {
            //delete everything
            for (var l = star_viewer.particles.length, i=l-1; i >= 0; i--)
                star_viewer.scene.removeObject(star_viewer.particles[i]);
            star_viewer.is_rendered = false;
        }
        star_viewer.particles = [];

        var material, particle, obj, color;
        if (star_viewer.show_sun) {
        //Staring sun
            material = new THREE.ParticleBasicMaterial( {
                map: new THREE.Texture( star_viewer.generateSunTexture(0xfff2a1,4) ), blending: THREE.AdditiveBlending
            } );
            particle = new THREE.Particle( material );
            particle.position.x = 0;
            particle.position.y = 0;
            particle.position.z = 0;
            particle.scale.x = particle.scale.y = particle.scale.z = .3;
            particle.isClickable = false;
            particle.name = "Sol";
            particle.starid = 0;
            star_viewer.scene.addObject( particle );
            star_viewer.particles.push( particle );
        }

        //Stars
        for ( var i = 0; i < show_amount-1; i ++ ) {
            if (i >= stars.length) break;
            obj = stars[i];
//            if (isHideDwarfs && (obj.starType.charAt(0) == "M")) continue; //Hide M-type stars
            color = parseInt(obj.web_color.replace("#",""),16) - color_offset;

            material = new THREE.ParticleBasicMaterial( {
                map: new THREE.Texture( star_viewer.generateSunTexture(color,1) ), blending: THREE.AdditiveBlending
            } );

            scale = star_viewer.size_based_on_star_mass(obj.mass);

            var location = {x:obj.x, y:obj.y, z:obj.z};
            if (star_viewer.central_sun && star_viewer.central_sun.x) {
                location.x -= star_viewer.central_sun.x;
                location.y -= star_viewer.central_sun.y;
                location.z -= star_viewer.central_sun.z;
            }

            particle = new THREE.Particle( material );
            particle.position = new THREE.Vector3( location.x, location.y, location.z );
            particle.scale.x = particle.scale.y = particle.scale.z = scale;
            particle.isClickable = true;
            particle.color = (color);
            particle.starid = i;
            particle.name = obj.name;
            star_viewer.scene.addObject( particle );
            star_viewer.particles.push( particle );
        }

    }
    star_viewer.is_rendered = true;
};
star_viewer.size_based_on_star_mass=function(mass){
    var scale = star_viewer.star_scale_default;
    if (mass){
        scale = star_viewer.star_scale_default + ((mass-1)/star_viewer.mass_rescale);
        if (scale > (2*star_viewer.star_scale_default)) scale = star_viewer.star_scale_default*2;
        if (scale < (.5*star_viewer.star_scale_default)) scale = star_viewer.star_scale_default*.5;
    }
    return scale;
};

function objectWasClicked(intersectClicked) {
    var starscopy = [];
    var objectClicked = intersectClicked.object;

    star_viewer.div_info.innerHTML=objectClicked.name;
    if (star_viewer.option_RenderEngine == "webgl") {
        if (star_viewer.lastClicked) {
            intersectClicked.star_viewer.particlesystem.geometry.colors[star_viewer.lastClicked] = new THREE.Color( star_viewer.lastColor );
            star_viewer.scene.removeObject(star_viewer.highlightLine);
        }
        star_viewer.lastClicked = intersectClicked.particleNumber;
        star_viewer.lastColor = intersectClicked.star_viewer.particlesystem.geometry.colors[intersectClicked.particleNumber].hex;
        intersectClicked.star_viewer.particlesystem.geometry.colors[intersectClicked.particleNumber].setHex( 0xff0000 );

        starscopy = intersectClicked.star_viewer.particlesystem.geometry.vertices.concat([]); //copy the sorted array

    } else { // Canvas or SVG

        if (star_viewer.lastClicked) {
            star_viewer.lastClicked.materials[0] = new THREE.ParticleBasicMaterial( {
                map: new THREE.Texture( star_viewer.generateSunTexture(star_viewer.lastColor,1) ), blending: THREE.AdditiveBlending
            } );
//						star_viewer.lastClicked.scale.x = star_viewer.lastClicked.scale.y = .1;
            star_viewer.scene.removeObject(star_viewer.highlightLine);
        }
        star_viewer.lastClicked = objectClicked;
        star_viewer.lastColor = objectClicked.materials[0].color.hex;
        objectClicked.materials[0] = new THREE.ParticleBasicMaterial( {
            map: new THREE.Texture( star_viewer.generateSunTexture(star_viewer.lastColor,1,true,'rgba(125, 20, 0, 0.2)' ) ), blending: THREE.AdditiveBlending
        } );
//					objectClicked.scale.x = objectClicked.scale.y = .3;

        for (var j = 0, k = star_viewer.scene.objects.length; j<k; j++) {
            var scobj = star_viewer.scene.objects[j];
            if (scobj.isClickable && scobj instanceof THREE.Particle)
                starscopy = starscopy.concat(scobj);
        }

    }

    var closest_sorted = starscopy.sort( function ( a, b ) { return objectClicked.position.distanceTo (a.position)-objectClicked.position.distanceTo (b.position); } );

    var closest = [];
    for (var i = 0; i < (star_viewer.stars_to_show*3); i++) {
        //remove duplicate stars
        var star = closest_sorted[i];
        if (star.name != closest_sorted[i+1].name) {
            closest.push(closest_sorted[i]);
        }
        if (closest.length > star_viewer.stars_to_show) break;
    }

    document.getElementById("infolefttitle").innerHTML = "Neighbors:";

    var geometry = new THREE.Geometry();  //TODO: Not count system binaries
    //For the 4 nearest stars
    for (var i = 1; i <= star_viewer.stars_to_show; i++) {
        geometry.vertices.push( new THREE.Vertex( closest[0].position ) );
        geometry.vertices.push( new THREE.Vertex( closest[i].position ) );
        var star = stars[closest[i].starid];

        var doctab = document.getElementById("infotab"+i);

        var color = parseInt(star.web_color.replace("#",""),16);
        var colorstar = new THREE.Color( color );
        doctab.style.backgroundColor = colorstar.rgbaString;

        doctab.innerHTML = "<nobr>"+i+": "+star.name+"</nobr><br/>"
        doctab.innerHTML+= "ID: "+star.id+ " "+
            parseInt(closest[0].position.distanceTo(closest[i].position))+" Parsec away";
//					doctab.appendChild(star_viewer.generateSunTexture(star.color,.8));

    }
    var material = new THREE.LineBasicMaterial( { color: 0xff0000, opacity: 0.6 } );
    star_viewer.highlightLine = new THREE.Line( geometry, material );
    star_viewer.scene.addObject( star_viewer.highlightLine );

};

//=========================================
star_viewer.init_grid=function() {
    // Grid
    var geometry = new THREE.Geometry();
    geometry.vertices.push( new THREE.Vertex( new THREE.Vector3( -1 * star_viewer.bounds, 0, 0 ) ) );
    geometry.vertices.push( new THREE.Vertex( new THREE.Vector3( star_viewer.bounds, 0, 0 ) ) );

    var material = new THREE.LineBasicMaterial( { color: 0x888888, opacity: 0.8 } );
    var lineSteps = 10;
    for ( var i = 0; i <= lineSteps; i ++ ) {
        var step = (200 *2) / lineSteps;

        var line = new THREE.Line( geometry, material );
        line.position.y = 0;
        line.position.z = ( i * step ) - 200;
        star_viewer.scene.addObject( line );

        var line = new THREE.Line( geometry, material );
        line.position.x = ( i * step ) - 200;
        line.position.y = 0;
        line.rotation.y = Math.PI / 2;
        star_viewer.scene.addObject( line );

    }
    console.log('Grid created and added to star_viewer.scene.  star_viewer.sceneObjects now:'+star_viewer.scene.objects.length);
};
star_viewer.init_camera=function() {
    star_viewer.camera = new THREE.Camera( 60, window.innerWidth / window.innerHeight, 1, 10000 );

    star_viewer.camera.position.y = star_viewer.bounds/7;
    star_viewer.camera.position.z = star_viewer.bounds/7;
    window.addEventListener( 'resize', onWindowResize, false );

    star_viewer.projector = new THREE.Projector();
    star_viewer.cameraControl = new CameraControlWASD( star_viewer.camera, star_viewer.camera_movement_speed, star_viewer.camera_look_speed, true, false, false, false );
};
star_viewer.init_stats=function() {
    star_viewer.stats = new Stats();
    star_viewer.stats.domElement.style.position = 'absolute';
    star_viewer.stats.domElement.style.top = '0px';
    star_viewer.container.appendChild( star_viewer.stats.domElement );
};

star_viewer.queryString=function(q) {
    hu = window.location.search.substring(1);
    gy = hu.split("&");
    var result = null;
    for (i=0;i<gy.length;i++) {
        ft = gy[i].split("=");
        if (ft[0] == q) {
            result = ft[1]; break;
        }
    }
    return result;
};
star_viewer.init_renderer=function() {
    star_viewer.renderer_created = false;
    var requested_renderer = star_viewer.queryString("renderer");
    if (!requested_renderer) requested_renderer="canvas";
    try {
        switch(requested_renderer) {
            case "webgl": star_viewer.renderer = new THREE.WebGLRenderer(); break;
            case "canvas": star_viewer.renderer = new THREE.CanvasRenderer(); break;
            case "svg": star_viewer.renderer = new THREE.SVGRenderer(); break;
            case "dom": star_viewer.renderer = new THREE.DOMRenderer(); break;
            default: break;
        }
        star_viewer.option_RenderEngine = requested_renderer;
        console.log('Rendering: '+requested_renderer);
        star_viewer.renderer_created = true;
    } catch (err) {
        //Try canvas
        console.log("WebGL Rendering failed");
        star_viewer.renderer = new THREE.CanvasRenderer();
        console.log('Rendering: Canvas');
        star_viewer.option_RenderEngine = "canvas";
        star_viewer.renderer_created = true;
    }

    if (star_viewer.renderer_created) {
        star_viewer.renderer.setSize( window.innerWidth, window.innerHeight );
        star_viewer.container.appendChild( star_viewer.renderer.domElement );
    } else {
        star_viewer.container.innerHTML = "<br/><br/><br/><h1>3D Rendering could not load</h1>";
        console.log("FAIL! No star_viewer.renderer able to load");
    }
};

function onWindowResize( event ) {
    //When rotated, resize the window and rendering space

    var width = window.innerWidth, height = window.innerHeight;

    star_viewer.camera.aspect = width / height;
    star_viewer.camera.updateProjectionMatrix();

    star_viewer.renderer.setSize( width, height );
    star_viewer.renderer.domElement.style.width = window.innerWidth + 'px';
    star_viewer.renderer.domElement.style.height = window.innerHeight + 'px';
}
star_viewer.animate=function() {
    //Animate these as often as possible - up to 60fps
    star_viewer.cameraControl.update();
    requestAnimationFrame( star_viewer.animate );
    star_viewer.render();
    star_viewer.stats.update();

};
star_viewer.render=function() {
    //Render the updated canvas
    star_viewer.renderer.render( star_viewer.scene, star_viewer.camera );
};
star_viewer.info=function(){
    var loc = star_viewer.central_sun;
    for (var i=0; i < stars.length; i++){
        var star = stars[i];
        var xd = star.x - loc.x;
        var yd = star.y - loc.y;
        var zd = star.z - loc.z;

        var dist = Math.sqrt(xd*xd + yd*yd + zd*zd);

        console.log(star.x+' '+star.y+' '+star.z+' : '+dist);
    }
};