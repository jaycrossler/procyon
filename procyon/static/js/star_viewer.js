var container, stats, div_details, div_info;
var camera, cameraControl, scene, renderer, projector;
var option_RenderEngine;

var is_rendered = false, particles = [];
var lastClicked = null, lastColor = null, highlightLine = null;

var PI2 = Math.PI * 2;
var program = function ( context, color ) {
    context.fillStyle = color.__styleString;
    context.beginPath();
    context.arc( 0, 0, 1, 0, PI2, true );
    context.closePath();
    context.fill();
}

function preloader() {
    init(); //Set up the scene and renderer
    animate(); //Start updating the scene as often as possible
}

function init() {
    container = document.getElementById( 'container'  );
    div_details =document.getElementById( 'details' );
    div_info= document.getElementById( 'info' );

    scene = new THREE.Scene();
    init_camera();
    init_grid();
    init_renderer();
    init_stats();

    init_object_points(100,false,true);
}
//=======================================
function generateSunTexture(color, size, showShell) {
    var size = (size) ? parseInt(size*24) : 24;
    var showShell = (showShell) ? showShell : false;
    var canvas = document.createElement( 'canvas' );
    canvas.width = size;
    canvas.height = size;
    var col = new THREE.Color(color);

    var context = canvas.getContext( '2d' );
    var gradient = context.createRadialGradient( canvas.width / 2, canvas.height / 2, 0, canvas.width / 2, canvas.height / 2, canvas.width / 2 );
    gradient.addColorStop( 0, col.rgbaString);
    gradient.addColorStop( 0.1, col.rgbaString);
    gradient.addColorStop( 0.6, 'rgba(125, 20, 0, 0.2)' );
    if (showShell) {
        gradient.addColorStop( 0.88, 'rgba(0, 20, 0, 1)' );
        gradient.addColorStop( 0.9, 'rgba(255, 255, 255, 0.2)' );
    }
    gradient.addColorStop( .92, 'rgba(0,0,0,0)' );
    context.fillStyle = gradient;
    context.fillRect( 0, 0, canvas.width, canvas.height );
    return canvas;

}
function init_object_points(show_amount, isRedder, isHideDwarfs) {

    if (!show_amount) show_amount = star_init_list.length;
    var color_offset = (isRedder) ? 0x006050 : 0x000000;

    //currently, the particles are rendered differently
    if (option_RenderEngine == "webgl") {
        if (is_rendered) {
            //delete everything
            scene.removeObject(particles);
            is_rendered = false;
        }

        //Staring sun // TODO, Add a seperate sphere?
        var geometry = new THREE.Geometry();
// 					var vector = new THREE.Vertex( new THREE.Vector3( 0,0,0 ));
// 					vector.name = "Sol: The Sun";
// 					geometry.vertices.push( vector );
// 					geometry.colors[ 0 ] = new THREE.Color( 0xfff2a1 - color_offset );

        //Stars
        for ( var i = 0; i <= show_amount; i ++ ) {
            if (i >= star_init_list.length) break;
            var obj = star_init_list[i];
//            if (isHideDwarfs && (obj.starType.charAt(0) == "M")) continue; //Hide M-type stars
            vector = new THREE.Vertex(new THREE.Vector3( obj.x, obj.y, obj.z ));
            vector.name = obj.name;
            vector.starid = i;

            var color = parseInt(obj.web_color.replace("#",""),16) - color_offset;
            vector.color = (color);

            geometry.vertices.push( vector );
            geometry.colors.push( new THREE.Color( obj.color - color_offset ) );
        }
        //TODO: Scale based on size
        var sprite = ImageUtils.loadTexture( "textures/sprites/sun2.png" );
        var material = new THREE.ParticleBasicMaterial( { size: (.1 + Math.random()*.1), map: sprite, blending: THREE.AdditiveBlending, vertexColors: true } );

        particles = new THREE.ParticleSystem( geometry, material );
        particles.sortParticles = true;
        particles.isClickable = true;
        particles.updateMatrix();
        scene.addObject( particles );

    } else { //for Canvas and SVG
        if (is_rendered) {
            //delete everything
            for (var l = particles.length, i=l-1; i >= 0; i--)
                scene.removeObject(particles[i]);
            is_rendered = false;
        }
        particles = [];

        //Staring sun
        var material = new THREE.ParticleBasicMaterial( { map: new THREE.Texture( generateSunTexture(0xfff2a1,4) ), blending: THREE.AdditiveBlending } );
        var particle = new THREE.Particle( material );
        particle.position.x = 0;
        particle.position.y = 0;
        particle.position.z = 0;
        particle.scale.x = particle.scale.y = .3;
        particle.isClickable = false;
        particle.name = "Sol";
        particle.starid = 0;
        scene.addObject( particle );
        particles.push( particle );

        //Stars
        for ( var i = 0; i < show_amount-1; i ++ ) {
            if (i >= star_init_list.length) break;
            var obj = star_init_list[i];
//            if (isHideDwarfs && (obj.starType.charAt(0) == "M")) continue; //Hide M-type stars
            var color = parseInt(obj.web_color.replace("#",""),16) - color_offset;

            var material = new THREE.ParticleBasicMaterial( {
                map: new THREE.Texture( generateSunTexture(color,1) ), blending: THREE.AdditiveBlending
            } );

            var particle = new THREE.Particle( material );
            particle.position = new THREE.Vector3( obj.x, obj.y, obj.z );
            particle.scale.x = particle.scale.y = .1 + (Math.random()*.1);  //TODO: Scale proportionally
            particle.isClickable = true;
            particle.color = (color);
            particle.starid = i;
            particle.name = obj.name;
            scene.addObject( particle );
            particles.push( particle );
        }

    }

    is_rendered = true;

}
function objectWasClicked(intersectClicked) {
    var starscopy = [];
    var objectClicked = intersectClicked.object;

    div_info.innerHTML=objectClicked.name;
    if (option_RenderEngine == "webgl") {
        if (lastClicked) {
            intersectClicked.particleSystem.geometry.colors[lastClicked] = new THREE.Color( lastColor );
            scene.removeObject(highlightLine);
        }
        lastClicked = intersectClicked.particleNumber;
        lastColor = intersectClicked.particleSystem.geometry.colors[intersectClicked.particleNumber].hex;
        intersectClicked.particleSystem.geometry.colors[intersectClicked.particleNumber].setHex( 0xff0000 );

        starscopy = intersectClicked.particleSystem.geometry.vertices.concat([]); //copy the sorted array

    } else { // Canvas or SVG

        if (lastClicked) {
            lastClicked.materials[0] = new THREE.ParticleBasicMaterial( { map: new THREE.Texture( generateSunTexture(lastColor,1) ), blending: THREE.AdditiveBlending } );
//						lastClicked.scale.x = lastClicked.scale.y = .1;
            scene.removeObject(highlightLine);
        }
        lastClicked = objectClicked;
        lastColor = objectClicked.materials[0].color.hex;
        objectClicked.materials[0] = new THREE.ParticleBasicMaterial( { map: new THREE.Texture( generateSunTexture(0xff0000,1,true) ), blending: THREE.AdditiveBlending } );
//					objectClicked.scale.x = objectClicked.scale.y = .3;

        for (var j = 0, k = scene.objects.length; j<k; j++) {
            var scobj = scene.objects[j];
            if (scobj.isClickable && scobj instanceof THREE.Particle)
                starscopy = starscopy.concat(scobj);
        }

    }

    var closest_sorted = starscopy.sort( function ( a, b ) { return objectClicked.position.distanceTo (a.position)-objectClicked.position.distanceTo (b.position); } );

    var stars_to_show = 4;
    var closest = [];
    for (var i = 0; i < (stars_to_show*3); i++) {
        //remove duplicate stars
        var star = closest_sorted[i];
        if (star.name != closest_sorted[i+1].name) {
            closest.push(closest_sorted[i]);
        }
        if (closest.length > stars_to_show) break;
    }

    document.getElementById("infolefttitle").innerHTML = "Neighbors:";

    var geometry = new THREE.Geometry();  //TODO: Not count system binaries
    //For the 4 nearest stars
    for (var i = 1; i <= stars_to_show; i++) {
        geometry.vertices.push( new THREE.Vertex( closest[0].position ) );
        geometry.vertices.push( new THREE.Vertex( closest[i].position ) );
        var star = star_init_list[closest[i].starid];

        var doctab = document.getElementById("infotab"+i);

        var color = parseInt(star.web_color.replace("#",""),16);
        var colorstar = new THREE.Color( color );
        doctab.style.backgroundColor = colorstar.rgbaString;

        doctab.innerHTML = "<nobr>"+i+": "+star.name+"</nobr><br/>"
        doctab.innerHTML+= "ID: "+star.id+ " "+
            parseInt(closest[0].position.distanceTo(closest[i].position))+" LY away";
//					doctab.appendChild(generateSunTexture(star.color,.8));

    }
    var material = new THREE.LineBasicMaterial( { color: 0xff0000, opacity: 0.6 } );
    highlightLine = new THREE.Line( geometry, material );
    scene.addObject( highlightLine );

}

//=========================================
function init_grid() {
    // Grid
    var geometry = new THREE.Geometry();
    geometry.vertices.push( new THREE.Vertex( new THREE.Vector3( -1 * 200, 0, 0 ) ) );
    geometry.vertices.push( new THREE.Vertex( new THREE.Vector3( 200, 0, 0 ) ) );

    var material = new THREE.LineBasicMaterial( { color: 0x888888, opacity: 0.8 } );
    var lineSteps = 10;
    for ( var i = 0; i <= lineSteps; i ++ ) {
        var step = (200 *2) / lineSteps;

        var line = new THREE.Line( geometry, material );
        line.position.y = 0;
        line.position.z = ( i * step ) - 200;
        scene.addObject( line );

        var line = new THREE.Line( geometry, material );
        line.position.x = ( i * step ) - 200;
        line.position.y = 0;
        line.rotation.y = Math.PI / 2;
        scene.addObject( line );

    }
    console.log('Grid created and added to Scene.  SceneObjects now:'+scene.objects.length);
}
function init_camera() {
    camera = new THREE.Camera( 60, window.innerWidth / window.innerHeight, 1, 10000 );

    camera.position.y = 30;
    camera.position.z = 30;
    window.addEventListener( 'resize', onWindowResize, false );

    projector = new THREE.Projector();
    cameraControl = new CameraControlWASD( camera, 10, 0.005, true, false, false, false );
}
function init_stats() {
    stats = new Stats();
    stats.domElement.style.position = 'absolute';
    stats.domElement.style.top = '0px';
    container.appendChild( stats.domElement );
}

function queryString(q) {
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
}
function init_renderer() {
    var renderer_created = false;
    var requested_renderer = queryString("renderer");
    if (!requested_renderer) requested_renderer="canvas";
    try {
        switch(requested_renderer) {
            case "webgl": renderer = new THREE.WebGLRenderer(); break;
            case "canvas": renderer = new THREE.CanvasRenderer(); break;
            case "svg": renderer = new THREE.SVGRenderer(); break;
            case "dom": renderer = new THREE.DOMRenderer(); break;
            default: break;
        }
        option_RenderEngine = requested_renderer;
        console.log('Rendering: '+requested_renderer);
        renderer_created = true;
    } catch (err) {
        //Try canvas
        console.log("WebGL Rendering failed");
        renderer = new THREE.CanvasRenderer();
        console.log('Rendering: Canvas');
        option_RenderEngine = "canvas";
        renderer_created = true;
    }

    if (renderer_created) {
        renderer.setSize( window.innerWidth, window.innerHeight );
        container.appendChild( renderer.domElement );
    } else {
        container.innerHTML = "<br/><br/><br/><h1>3D Rendering could not load</h1>";
        console.log("FAIL! No renderer able to load");
    }
}

function onWindowResize( event ) {
    //When rotated, resize the window and rendering space

    var width = window.innerWidth, height = window.innerHeight;

    camera.aspect = width / height;
    camera.updateProjectionMatrix();

    renderer.setSize( width, height );
    renderer.domElement.style.width = window.innerWidth + 'px';
    renderer.domElement.style.height = window.innerHeight + 'px';
}
function animate() {
    //Animate these as often as possible - up to 60fps
    cameraControl.update();
    requestAnimationFrame( animate );
    render();
    stats.update();

}
function render() {
    //Render the updated canvas
    renderer.render( scene, camera );
}