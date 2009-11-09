<html xmlns:py="http://purl.org/kid/ns#">
   <body>
      <ul py:def="display_tree(tree)">
         <li>
         ${tree.name}
         <div py:for="item in tree.children" py:replace="display_tree(item)" />
         </li>
      </ul>
      
      <div py:replace="display_tree(tree)">
         Key/Value Table replaces this text
      </div>
      
   </body>
</html>
