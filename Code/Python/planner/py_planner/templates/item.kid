<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Welcome to TurboGears</title>
</head>

<body>
    
<h2 py:content="title">Title Here</h2>

<div class="description" py:content="description">
Main Description Here.
</div>

<div class="note" py:for="note in notes" py:content="note.content">
Note here
</div>

    
</body>
</html>