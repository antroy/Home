
(defun sum-even-fibs (fib-gen max-size)
  (setf next (funcall fib-gen))
  (if (< next max-size)
      (if (= 0 (mod next 2))
        (+ next (sum-even-fibs fib-gen max-size))
        (sum-even-fibs fib-gen max-size))
      0))



