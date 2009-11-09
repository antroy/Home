;(println "Hello World")

;(println (first *command-line-args*))
;(println (rest *command-line-args*))

;(defn parse [coll]
;  (map #(do (println %)) coll))
;

(defstruct option :short :long :desc :argcount)

(defn parse [options args]
  (if (not (empty? args)) 
    (do 
      () 
      (recur (rest args)))))

(def options 
  [
   (struct option "-f" "--file" "Filename pattern to find" 1)
   (struct option "-a" "--archives" "Descend into archives")
 ]
)


(parse options (rest *command-line-args*))
