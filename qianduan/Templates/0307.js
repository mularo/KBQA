// //javescript文件需要在浏览器中才能生效，在html前端文件中加上这个文件的路径可以实现
// // 使用jQuery库的$.getJSON()函数异步请求JSON数据
// $.getJSON('/get_knowledge_subgraph', {entity: '油箱'}, function(data) {
//   // 遍历JSON数据中的节点信息，并使用D3.js等可视化库在页面上展示出来
//   data.nodes.forEach(function(node) {
//     // 在页面上添加节点
//     var nodeElement = $('<div class="node">' + node.label + '</div>');
//     $('body').append(nodeElement);
//   });
//
//   // 遍历JSON数据中的边信息，并使用D3.js等可视化库在页面上展示出来
//   data.edges.forEach(function(edge) {
//     // 在页面上添加边
//     var sourceNode = $('.node').eq(edge.source - 1);
//     var targetNode = $('.node').eq(edge.target - 1);
//     var edgeElement = $('<div class="edge">' + edge.label + '</div>');
//     sourceNode.append(edgeElement);
//   });
// });

$(document).ready(function() {
  $('#function-btn').click(function() {
    $.ajax({
      type: "POST",
      url: "/get_function_graph",
      success: function(result) {
        $('#result').html(result);
      }
    });
  });
  $('#incident-btn').click(function() {
    $.ajax({
      type: "POST",
      url: "/get_incident_graph",
      success: function(result) {
        $('#result').html(result);
      }
    });
  });
  $('#damage-tree-btn').click(function() {
    $.ajax({
      type: "POST",
      url: "/get_damage_tree_graph",
      success: function(result) {
        $('#result').html(result);
      }
    });
  });
});
