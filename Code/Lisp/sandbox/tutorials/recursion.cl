;; Remove Elements

(defun remove-elements (elmt lst)
  (cond ((null lst) ())
        ((equal elmt (first lst))  (remove-elements elmt (rest lst))) 
        (t (cons (first lst) (remove-elements elmt (rest lst))))
  )
)

(defun test1 ()
  (print
    (remove-elements 'hello '(hello why dont you say hello))
  ))  

;; Functional Fibbonnacci

(defun fib (f s max-n)
  (if (> s max-n) 
    s
    (fib s (+ f s) max-n)))

(defun fib-n (max-n)
  (fib 1 1 max-n))
   
(defun test2 ()
  (print (fib-n 10)))
 
;; Fibbonnacci Generator

(defun fibgen (a b)
    (lambda () 
        (setf z a)
        (setf a b)
        (setf b (+ z b))
         b))


(defun test3 ()
  (setf fibonacci (fibgen 1 1))
  (print (funcall fibonacci))
  (print (funcall fibonacci))
  (print (funcall fibonacci))
  (print (funcall fibonacci))
  (print (funcall fibonacci))
  )

 
;; Run Tests.
(test1)
(test2)
(test3)




