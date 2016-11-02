// Convert rgb to hex for CSS

var rgbToCssColor_ = function(red, green, blue) {
  var rgbNumber = new Number((red << 16) | (green << 8) | blue);
  var hexString = rgbNumber.toString(16);
  var missingZeros = 6 - hexString.length;
  var resultBuilder = ['#'];
  for (var i = 0; i < missingZeros; i++) {
     resultBuilder.push('0');
  }
  resultBuilder.push(hexString);
  return resultBuilder.join('');
};
