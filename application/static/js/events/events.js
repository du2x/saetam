'use strict';

var base_url = '/';

angular.module('myApp.events', ['ngRoute', 'ngMaterial'])
.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/events', {
        templateUrl: '/js/events/events.html',
        controller: 'EventsCtrl',
    })
    .when('/events/:eventId/edit', {
        templateUrl: '/js/events/eventEdit.html',
        controller: 'EventEditCtrl as ctrl',
    })
    .when('/events/new', {
        templateUrl: '/js/events/eventEdit.html',  
        controller: 'EventEditCtrl as ctrl'      
    })    
}])
.factory('events', function($http){
    return{
        list: function(callback){
            $http.get('/events').success(callback);
        }                    
    }
})
.factory('event', function($http){
    return{
        obj: function(event_id, callback){
            $http.get('/events/' + event_id).success(callback);
        }                    
    }
})
.controller('EventsCtrl', function($scope, $http, events) {	
    events.list(function(data){
        $scope.events = data['data'];
    });
})
.controller('EventDetailCtrl', function($scope, $http, $routeParams, event) { 
    event.obj($routeParams.eventId, function(data){
        $scope.event = data['data'];
    });
})
.controller('EventEditCtrl', function($scope, $http, $routeParams, $location, $log, event) { 
    var self = this;
    var isNew = false;
    if($routeParams.eventId==undefined){
        isNew = true;
    }

    if(!isNew){
        event.obj($routeParams.eventId, function(data){
            $scope.event = data['data'];  
            $scope.event.event_date = new Date($scope.event.event_date);
            var updateCities = function(){                
                $http.get('/states/' + $scope.event.event_state + '/cities')
                    .success(function(data){            
                        self.cities = data['data'].map(function (city) {
                            return {
                                value: city.toLowerCase(),
                                display: city
                            };
                        });
                    })
            };
            updateCities();    
        });
    }


  $scope.state_selected = function(){                
            $http.get('/states/' + $scope.event.event_state + '/cities')
                .success(function(data){            
                    // workarround clear event city autocomplete field
                    $scope.event.event_city = '';
                    $scope.ctrl.searchText = '';                    
                    self.cities = data['data'].map(function (city) {
                        return {
                            value: city.toLowerCase(),
                            display: city
                        };
                    });
                })
        }

  $scope.saveEvent = function(event){
    if(event.id!=undefined){
        $http.post('/events/'+event.id+'/update', event)
            .success(function(data){            
                $location.path('#/events');
            });
    }
    else {
        $http.post('/events/insert', event)
            .success(function(data){            
                $location.path('#/events');
            });
    }
  };            

  // Autocomplete
  self.isDisabled    = false;
  // list of `state` value/display objects
  self.cities        = [];
  self.querySearch   = querySearch;
  self.selectedItemChange = selectedItemChange;
  self.searchTextChange   = searchTextChange;

    function querySearch (query) {
      var results = query ? self.cities.filter( createFilterFor(query) ) : self.cities, deferred;
      return results;
    }

    function createFilterFor(query) {
      var lowercaseQuery = angular.lowercase(query);
      return function filterFn(city) {
        return (city.value.indexOf(lowercaseQuery) === 0);
      };
    }

    function searchTextChange(text) {
      $log.info('Text changed to ' + text);
    }

    function selectedItemChange(item) {
        if(item!=undefined && item.display!=undefined) {
            $scope.event.event_city = item.display;
            console.log(item);
        }
       $log.info('Item changed to ' + JSON.stringify(item)); 
    }
});