;; Non-tail recursive:

(defun list-add (numbers)
  (cond ((null numbers) 0)
        (T (+ (first numbers) (list-add (rest numbers))))))

;; tail-recursive

(defun list-add2 (numbers &key (total 0))
  (cond ((null numbers) total)
        ( T (list-add2 (rest numbers) :total (+ (first numbers) total)))))



