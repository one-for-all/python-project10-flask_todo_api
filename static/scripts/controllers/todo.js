'use strict';

angular.module('todoListApp')
.controller('todoCtrl', function($scope, Todo) {
  $scope.deleteTodo = function(todo, index) {
    $scope.todos.splice(index, 1);
    console.log(todo)
    todo.$delete();
  };
  
  $scope.saveTodos = function() {
    var filteredTodos = $scope.todos.filter(function(todo){
      if(todo.edited) {
        return todo;
      };
    });
    filteredTodos.forEach(function(todo) {
      if (todo.id) {
        console.log(todo)
        todo.$update();
      } else {
        console.log(todo)
        todo.$save();
      }
    });
  }; 
});