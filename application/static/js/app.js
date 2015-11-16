'use strict';
// Declare app level module which depends on views, and components
angular.module('myApp', [
  'ngRoute',
  'ngMaterial',
  'myApp.events',
])
.config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/events'});
}])
/*.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}])
*/
.controller('AppCtrl', ['$scope', '$mdSidenav', function($scope, $mdSidenav){
  $scope.toggleSidenav = function(menuId) {
    $mdSidenav(menuId).toggle();
  }
  $scope.back = function() { 
    window.history.back();
  }; 
  $scope.states = [['AC','Acre'],['AL','Alagoas'],['AM','Amazonas'],
    ['AP','Amapá'],['BA','Bahia'],['CE','Ceará'],
    ['DF','Distrito Federal'],['ES','Espírito Santo'],['GO','Goiás'],
    ['MA','Maranhão'],['MG','Minas Gerais'],['MS','Mato Grosso do Sul'],
    ['MT','Mato Grosso'],['PA','Pará'],['PB','Paraíba'],
    ['PE','Pernambuco'],['PI','Piauí'],['PR','Paraná'],
    ['RJ','Rio de Janeiro'],['RN','Rio Grande do Norte'],['RO','Rondônia'],
    ['RR','Roraima'],['RS','Rio Grande do Sul'],['SC','Santa Catarina'],
    ['SE','Sergipe'],['SP','São Paulo'],['TO','Tocantins']
  ];

  


}]);
