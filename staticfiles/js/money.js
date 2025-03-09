function _moneyFormat( _number , _milesSeparator, _decimalSeparator) {
    //var _separator = '.';
    //Aqui le sacamos el punto del mil para hacer las cuentas
    var _values = _number.toString().split( _milesSeparator );
    var i = 0;
    var numero = '';
    while (i<_values.length) {
          numero += _values[i];
          i++;
    }
    _values = numero.split( _decimalSeparator );
    var _fraction = '00';
    if (_values[ 1 ]) {
       if (_values[ 1 ].length >= 2) {
          _fraction = _values[ 1 ].substr( 0, 2 );
       }
       else if (_values[ 1 ].length == 1) {
          _fraction = _values[ 1 ] + '0';
       }
    }
    _number = _values[ 0 ] + '.' + _fraction;
    return _number;
 }

 function _giveMoneyFormat( _number , _milesSeparator, _decimalSeparatorOriginal, _decimalSeparatorAMostrar) {

    _values = _number.split( _decimalSeparatorOriginal );
    var _fraction = '00';
    if (_values[ 1 ]) {
       if (_values[ 1 ].length >= 2) {
          _fraction = _values[ 1 ].substr( 0, 2 );
       }
       else if (_values[ 1 ].length == 1) {
          _fraction = _values[ 1 ] + '0';
       }
    }
    //Aqui le ponemos el punto del mil para hacer las cuentas
    var numero = '';
    var i = 0;
    var nroOriginal = _values[0];
    while (i<nroOriginal.length) {
        if(i%3==0 && nroOriginal.charAt(nroOriginal.length -i -1)!='-' && i!=0) {
          numero = _milesSeparator + numero;
        }
          numero = nroOriginal.charAt(nroOriginal.length -i -1) + numero;
          i++;
    }
if (nroOriginal.length==0)
numero = 0;

    _number = numero + _decimalSeparatorAMostrar + _fraction;
    return _number;
 }

