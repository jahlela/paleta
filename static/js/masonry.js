// external js: masonry.pkgd.js

var grid = document.querySelector('.grid');

// layout Masonry after each image loads
$grid.imagesLoaded().progress( function() {
  $grid.masonry('layout');
});

var masonryOptions = {
  columnWidth: 130,
  itemSelector: '.grid-item'
}
// init Masonry
var $grid = $('.grid').masonry( masonryOptions );

var isActive = true;

$('.toggle-button').on( 'click', function() {
  if ( isActive ) {
    $grid.masonry('destroy');
  } else {
    // re-init Masonry
    $grid.masonry( masonryOptions );
  }
  isActive = !isActive;
});










grid.addEventListener( 'click', function( event ) {
  // don't proceed if item was not clicked on
  if ( !matchesSelector( event.target, '.grid-item' ) ) {
    return;
  }
  // change size of item via class
  event.target.classList.toggle('grid-item--gigante');
  // trigger layout
  msnry.layout();
});
