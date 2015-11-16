'use strict';

angular.module('myApp.tickets', ['ngRoute', 'ngMaterial'])
.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/events/:eventId/tickets', {
        templateUrl: '/webapp/tickets/tickets.html',
        controller: 'TicketsCtrl as ctrl',
    })
    .when('/events/:eventId/tickets/new', {
        templateUrl: '/webapp/tickets/ticketCreate.html',
        controller: 'TicketEditCtrl as ctrl',
    })
    .when('/events/:eventId/tickets/new', {
        templateUrl: '/webapp/tickets/ticketCreate.html',
        controller: 'TicketEditCtrl as ctrl',
    })    
}])
