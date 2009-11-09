
(defun intfib (mx &optional (series '(1 1)))
  (let ((next (+ (first series) (second series))))
  (if (>= next mx)
    series
    (progn 
      (push next series)
      (intfib mx series)))))

(defun fib (mx)
  (reverse (intfib mx)))


(defun filter (fn lst)
  (let ((out nil))
    (dolist (item lst)
      (if (funcall fn item)
        (push item out)))
    (reverse out)))


(defun evenfib (mx)
  (let ((fibs (fib mx)))
    (filter #'evenp fibs)))

(defun az (a &optional (b 7))
  (format t "A: ~A; B: ~A" a b))

(defun p2 () 
  (reduce #'+ (evenfib 1000000)))

;(format t "First 3: ~A" (fib '(1 2) 10))

;(format t "Hello World")
