
(defun fibgen (a b)
    (lambda () 
        (setf z a)
        (setf a b)
        (setf b (+ z b))
         b))

(defun fibgen2 ()
    (setf a 1 b 1)
    (lambda () 
        (setf z a)
        (setf a b)
        (setf b (+ z b))
         b))

(print  (fibgen 1 2))
