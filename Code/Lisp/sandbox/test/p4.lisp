(defun palin (num)
  (let ((nums (format nil "~A" num)))
    (equal (reverse nums) nums)))

(defun p4 nil
  (let ((biggest 0))
    (do ((x 100 (+ x 1))) ((>= x 1000))
      (do ((y 100 (+ y 1))) ((>= y 1000))
        (let ((prod (* x y)))
          (if (palin prod)
            (setf biggest 
                  (max prod biggest))))))
      biggest))
; Works but very slow compared to python version.
