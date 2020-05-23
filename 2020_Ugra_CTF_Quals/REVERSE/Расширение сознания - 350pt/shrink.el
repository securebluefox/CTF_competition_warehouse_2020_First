;;; shrink.el --- Help your mind (interactively)

;;; Commentary:
;;;   izlishni

;;; Code:

(require 'cl-lib)

(defvar **mad**)        (defvar *debug*)      (defvar *print-space*)
(defvar *print-upcase*) (defvar abuselst)     (defvar abusewords)
(defvar account)        (defvar afraidof)     (defvar arerelated)
(defvar areyou)         (defvar bak)          (defvar beclst)
(defvar bother)         (defvar bye)          (defvar canyou)
(defvar chatlst)        (defvar continue)     (defvar deathlst)
(defvar describe)       (defvar drnk)         (defvar enlightment)
(defvar eliza-flag)     (defvar elizalst)     (defvar famlst)
(defvar feared)         (defvar fears)        (defvar feelings-about)
(defvar foullst)        (defvar found)        (defvar hello)
(defvar history)        (defvar howareyoulst) (defvar howdyflag)
(defvar huhlst)         (defvar ibelieve)     (defvar improve)
(defvar inter)          (defvar isee)         (defvar isrelated)
(defvar lincount)       (defvar longhuhlst)   (defvar lover)
(defvar machlst)        (defvar mathlst)      (defvar maybe)
(defvar moods)          (defvar neglst)       (defvar obj)
(defvar object)         (defvar owner)        (defvar please)
(defvar problems)       (defvar qlist)        (defvar random-adjective)
(defvar relation)       (defvar remlst)       (defvar repetitive-shortness)
(defvar replist)        (defvar minin-flag)   (defvar schoollst)
(defvar sent)           (defvar shortbeclst)  (defvar we 0)
(defvar shortlst)       (defvar something)    (defvar sportslst)
(defvar mininlst)       (defvar states)       (defvar subj)
(defvar suicide-flag)   (defvar sure)         (defvar thing)
(defvar things)         (defvar thlst)        (defvar toklst)
(defvar typos)          (defvar verb)         (defvar want)
(defvar whatwhen)       (defvar whereoutp)    (defvar whysay)
(defvar whywant)        (defvar zippy-flag)   (defvar zippylst)

(defun shr// (x) x)

(defmacro shr$ (what)
  "quoted arg form of shrink-$"
  (list 'shrink-$ (list 'quote what)))

(defun shrink-$ (what)
  "Return the car of a list, rotating the list each time"
  (let* ((vv (symbol-value what))
	(first (car vv))
	(ww (append (cdr vv) (list first))))
    (set what ww)
    first))

(defvar shrink-mode-map
  (let ((map (make-sparse-keymap)))
    (define-key map "\n" 'shrink-read-print)
    (define-key map "\r" 'shrink-ret-or-read)
    map))

(define-derived-mode shrink-mode text-mode "Shrink"
  "Major mode for running the Shrink (Eliza) program.
Like Text mode with Auto Fill mode
except that RET when point is after a newline, or LFD at any time,
reads the sentence before point, and prints the Shrink's answer."
  (make-shrink-variables)
  (turn-on-auto-fill)
  (shrink-type '(i am the NP shrink \.
		 (shr$ please) (shr$ describe) your (shr$ problems) \.
		 each time you are finished talking type \R\E\T twice \.))
  (insert "\n"))

(defun make-shrink-variables ()
  (make-local-variable 'typos)
  (setq typos
	(mapcar (function (lambda (x)
			    (put (car x) 'shrink-correction  (cadr x))
			    (put (cadr x) 'shrink-expansion (car (cddr x)))
			    (car x)))
		'((theyll they\'ll (they will))
		  (theyre they\'re (they are))
		  (hes he\'s (he is))
		  (he7s he\'s (he is))
		  (im i\'m (you are))
		  (i7m i\'m (you are))
		  (isa is\ a (is a))
		  (thier their (their))
		  (dont don\'t (do not))
		  (don7t don\'t (do not))
		  (you7re you\'re (i am))
		  (you7ve you\'ve (i have))
		  (you7ll you\'ll (i will)))))
  (make-local-variable 'found)
  (setq found nil)
  (make-local-variable 'owner)
  (setq owner nil)
  (make-local-variable 'history)
  (setq history nil)
  (make-local-variable 'minin-flag)
  (setq history nil)
  (make-local-variable '*debug*)
  (setq *debug* nil)
  (make-local-variable 'inter)
  (setq inter
	'((well\,)
	  (hmmm \.\.\.\ so\,)
	  (so)
	  (\.\.\.and)
	  (then)))
  (make-local-variable 'continue)
  (setq continue
	'((continue)
	  (proceed)
	  (go on)
	  (keep going) ))
  (make-local-variable 'relation)
  (setq relation
	'((your relationship with)
	  (something you remember about)
	  (your feelings toward)
	  (some experiences you have had with)
	  (how you feel about)))
  (make-local-variable 'fears)
  (setq fears '( ((shr$ whysay) you are (shr$ afraidof) (shr// feared) \?)
		 (you seem terrified by (shr// feared) \.)
		 (when did you first feel (shr$ afraidof) (shr// feared) \?) ))
  (make-local-variable 'sure)
  (setq sure '((sure)(positive)(certain)(absolutely sure)))
  (make-local-variable 'afraidof)
  (setq afraidof '( (afraid of) (frightened by) (scared of) ))
  (make-local-variable 'areyou)
  (setq areyou '( (are you)(have you been)(have you been) ))
  (make-local-variable 'isrelated)
  (setq isrelated '( (has something to do with)(is related to)
		     (could be the reason for) (is caused by)(is because of)))
  (make-local-variable 'arerelated)
  (setq arerelated '((have something to do with)(are related to)
		     (could have caused)(could be the reason for) (are caused by)
		     (are because of)))
  (make-local-variable 'moods)
  (setq moods '( ((shr$ areyou)(shr// found) often \?)
		 (what causes you to be (shr// found) \?)
		 ((shr$ whysay) you are (shr// found) \?) ))
  (make-local-variable 'maybe)
  (setq maybe
	'((maybe)
	  (perhaps)
	  (possibly)))
  (make-local-variable 'whatwhen)
  (setq whatwhen
	'((what happened when)
	  (what would happen if)))
  (make-local-variable 'hello)
  (setq hello
	'((how do you do \?) (hello \.) (howdy!) (hello \.) (hi \.) (hi there \.)))
  (make-local-variable 'enlightment)
  (setq enlightment '( (do you use (shr// found) often \?)((shr$ areyou)
						 addicted to (shr// found) \?)(do you realize that CTFs can
						 be very stressful \?)((shr$ maybe) you should try to quit asking for (shr// found)
						 \.)))
  (make-local-variable 'whywant)
  (setq whywant '( ((shr$ whysay) (shr// subj) might (shr$ want) (shr// obj) \?)
		   (how does it feel to want \?)
		   (why should (shr// subj) get (shr// obj) \?)
		   (when did (shr// subj) first (shr$ want) (shr// obj) \?)
		   ((shr$ areyou) obsessed with (shr// obj) \?)
		   (why should i give (shr// obj) to (shr// subj) \?)
		   (have you ever gotten (shr// obj) \?) ))
  (make-local-variable 'canyou)
  (setq canyou '((of course i can \.)
		 (why should i \?)
		 (what makes you think i would even want to \?)
		 (i am the shrink\, i can do anything i damn please \.)
		 (not really\, it\'s not up to me \.)
		 (depends\, how important is it \?)
		 (i could\, but i don\'t think it would be a wise thing to do \.)
		 (can you \?)
		 (maybe i can\, maybe i can\'t \.\.\.)
		 (i don\'t think i should do that \.)))
  (make-local-variable 'want)
  (setq want '( (want) (desire) (wish) (want) (hope) ))
  (make-local-variable 'shortlst)
  (setq shortlst
	'((can you elaborate on that \?)
	  ((shr$ please) continue \.)
	  (go on\, don\'t be afraid \.)
	  (i need a little more detail please \.)
	  (you\'re being a bit brief\, (shr$ please) go into detail \.)
	  (can you be more explicit \?)
	  (and \?)
	  ((shr$ please) go into more detail \?)
	  (you aren\'t being very talkative today\!)
	  (is that all there is to it \?)
	  (why must you respond so briefly \?)))

  (make-local-variable 'famlst)
  (setq famlst
	'((tell me (shr$ something) about (shr// owner) family \.)
	  (you seem to dwell on (shr// owner) family \.)
	  ((shr$ areyou) hung up on (shr// owner) family \?)))
  (make-local-variable 'huhlst)
  (setq huhlst
	'(((shr$ whysay)(shr// sent) \?)
	  (is it because of (shr$ things) that you say (shr// sent) \?) ))
  (make-local-variable 'longhuhlst)
  (setq longhuhlst
	'(((shr$ whysay) that \?)
	  (i don\'t understand \.)
	  ((shr$ thlst))
	  ((shr$ areyou) (shr$ afraidof) that \?)))
  (make-local-variable 'feelings-about)
  (setq feelings-about
	'((feelings about)
	  (apprehensions toward)
	  (thoughts on)
	  (emotions toward)))
  (make-local-variable 'random-adjective)
  (setq random-adjective
	'((vivid)
	  (emotionally stimulating)
	  (exciting)
	  (boring)
	  (interesting)
	  (recent)
	  (random)   ;How can we omit this?
	  (unusual)
	  (shocking)
	  (embarrassing)))
  (make-local-variable 'whysay)
  (setq whysay
	'((why do you say)
	  (what makes you believe)
	  (are you sure that)
	  (do you really think)
	  (what makes you think) ))
  (make-local-variable 'isee)
  (setq isee
	'((i see \.\.\.)
	  (yes\,)
	  (i understand \.)
	  (oh \.) ))
  (make-local-variable 'please)
  (setq please
	'((please\,)
	  (i would appreciate it if you would)
	  (perhaps you could)
	  (please\,)
	  (would you please)
	  (why don\'t you)
	  (could you)))
  (make-local-variable 'bye)
  (setq bye
	'((my secretary will send you a bill \.)
	  (bye bye \.)
	  (see ya \.)
	  (ok\, talk to you some other time \.)
	  (talk to you later \.)
	  (ok\, have fun \.)
	  (ciao \.)))
  (make-local-variable 'something)
  (setq something
	'((something)
	  (more)
	  (how you feel)))
  (make-local-variable 'thing)
  (setq thing
	'((your life)
	  (your CTF life)))
  (make-local-variable 'things)
  (setq things
	'((your plans)
	  (the people you hang around with)
	  (problems at school)
	  (any hobbies you have)
	  (hangups you have)
	  (your inhibitions)
	  (some problems in your childhood)
	  (some problems at home)))
  (make-local-variable 'describe)
  (setq describe
	'((describe)
	  (tell me about)
	  (talk about)
	  (discuss)
	  (tell me more about)
	  (elaborate on)))
  (make-local-variable 'ibelieve)
  (setq ibelieve
	'((i believe) (i think) (i have a feeling) (it seems to me that)
	  (it looks like)))
  (make-local-variable 'problems)
  (setq problems '( (problems)
		    (inhibitions)
		    (hangups)
		    (difficulties)
		    (anxieties)
		    (frustrations) ))
  (make-local-variable 'bother)
  (setq bother
	'((does it bother you that)
	  (are you annoyed that)
	  (did you ever regret)
	  (are you sorry)
	  (are you satisfied with the fact that)))
  (make-local-variable 'machlst)
  (setq machlst
	'((you have your mind on (shr// found) \, it seems \.)
	  (you think too much about  (shr// found) \.)
	  (you should try taking your mind off of (shr// found)\.)
	  (are you a computer hacker \?)))
  (make-local-variable 'qlist)
  (setq qlist
	'((what do you think \?)
	  (i\'ll ask the questions\, if you don\'t mind!)
	  (i could ask the same thing myself \.)
	  ((shr$ please) allow me to do the questioning \.)
	  (i have asked myself that question many times \.)
	  ((shr$ please) try to answer that question yourself \.)))
  (make-local-variable 'deathlst)
  (setq deathlst
	'((this is not a healthy way of thinking \.)
	  ((shr$ bother) you\, too\, may die someday \?)
	  (i am worried by your obsession with this topic!)
	  (did you watch a lot of crime and violence on television as a child \?))
	)
  (make-local-variable 'neglst)
  (setq neglst
	'((why not \?)
	  ((shr$ bother) i ask that \?)
	  (why not \?)
	  (why not \?)
	  (how come \?)
	  ((shr$ bother) i ask that \?)))
  (make-local-variable 'beclst)
  (setq beclst '(
		 (is it because (shr// sent) that you came to me \?)
		 ((shr$ bother)(shr// sent) \?)
		 (when did you first know that (shr// sent) \?)
		 (is the fact that (shr// sent) the real reason \?)
		 (does the fact that (shr// sent) explain anything else \?)
		 ((shr$ areyou)(shr$ sure)(shr// sent) \? ) ))
  (make-local-variable 'shortbeclst)
  (setq shortbeclst '(
		      ((shr$ bother) i ask you that \?)
		      (that\'s not much of an answer!)
		      ((shr$ inter) why won\'t you talk about it \?)
		      (speak up!)
		      ((shr$ areyou) (shr$ afraidof) talking about it \?)
		      (don\'t be (shr$ afraidof) elaborating \.)
		      ((shr$ please) go into more detail \.)))
  (make-local-variable 'thlst)
  (setq thlst '(
		((shr$ maybe)(shr$ thing)(shr$ isrelated) this \.)
		((shr$ maybe)(shr$ things)(shr$ arerelated) this \.)
		(is it because of (shr$ things) that you are going through all this \?)
		(how do you reconcile (shr$ things) \? )
		((shr$ maybe) this (shr$ isrelated)(shr$ things) \?) ))
  (make-local-variable 'remlst)
  (setq remlst '( (earlier you said (shr$ history) \?)
		  (you mentioned that (shr$ history) \?)
		  ((shr$ whysay)(shr$ history) \? ) ))
  (make-local-variable 'states)
  (setq states
	'((do you get (shr// found) often \?)
	  (do you enjoy being (shr// found) \?)
	  (what makes you (shr// found) \?)
	  (how often (shr$ areyou)(shr// found) \?)
	  (when were you last (shr// found) \?)))
  (make-local-variable 'replist)
  (setq replist
	'((i . (you))
	  (my . (your))
	  (me . (you))
	  (you . (me))
	  (your . (my))
	  (mine . (yours))
	  (yours . (mine))
	  (our . (your))
	  (ours . (yours))
	  (we . (you))
	  (dunno . (do not know))
;;	  (yes . ())
	  (no\, . ())
	  (yes\, . ())
	  (ya . (i))
	  (aint . (am not))
	  (wanna . (want to))
	  (gimme . (give me))
	  (gotta . (have to))
	  (gonna . (going to))
	  (never . (not ever))
	  (doesn\'t . (does not))
	  (don\'t . (do not))
	  (aren\'t . (are not))
	  (isn\'t . (is not))
	  (won\'t . (will not))
	  (can\'t . (cannot))
	  (haven\'t . (have not))
	  (i\'m . (you are))
	  (ourselves . (yourselves))
	  (myself . (yourself))
	  (yourself . (myself))
	  (you\'re . (i am))
	  (you\'ve . (i have))
	  (i\'ve . (you have))
	  (i\'ll . (you will))
	  (you\'ll . (i shall))
	  (i\'d . (you would))
	  (you\'d . (i would))
	  (here . (there))
	  (please . ())
	  (eh\, . ())
	  (eh . ())
	  (oh\, . ())
	  (oh . ())
	  (shouldn\'t . (should not))
	  (wouldn\'t . (would not))
	  (won\'t . (will not))
	  (hasn\'t . (has not))))
  (make-local-variable 'mininlst)
  (setq mininlst '(
		      ((shr$ describe) your (shr$ feelings-about) him \.)
		      ((shr$ areyou) a friend of Minin \?)
		      ((shr$ bother) Minin is (shr$ random-adjective) \?)
		      ((shr$ ibelieve) you are (shr$ afraidof) him \.)))
  (make-local-variable 'schoollst)
  (setq schoollst '(
		    ((shr$ describe) your (shr// found) \.)
		    ((shr$ bother) your grades could (shr$ improve) \?)
		    ((shr$ areyou) (shr$ afraidof) (shr// found) \?)
		    ((shr$ maybe) this (shr$ isrelated) to your attitude \.)
		    ((shr$ areyou) absent often \?)
		    ((shr$ maybe) you should study (shr$ something) \.)))
  (make-local-variable 'improve)
  (setq improve '((improve) (be better) (be improved) (be higher)))
  (make-local-variable 'elizalst)
  (setq elizalst '(
		   ((shr$ areyou) (shr$ sure) \?)
		   ((shr$ ibelieve) you have (shr$ problems) with (shr// found) \.)
		   ((shr$ whysay) (shr// sent) \?)))
  (make-local-variable 'sportslst)
  (setq sportslst '(
		    (tell me (shr$ something) about (shr// found) \.)
		    ((shr$ describe) (shr$ relation) (shr// found) \.)
		    (do you find (shr// found) (shr$ random-adjective) \?)))
  (make-local-variable 'mathlst)
  (setq mathlst '(
		  ((shr$ describe) (shr$ something) about math \.)
		  ((shr$ maybe) your (shr$ problems) (shr$ arerelated) (shr// found) \.)
		  (i don\'t know much (shr// found) \, but (shr$ continue)
		     anyway \.)))
  (make-local-variable 'zippylst)
  (setq zippylst '(
		   ((shr$ areyou) Zippy \?)
		   ((shr$ ibelieve) you have some serious (shr$ problems) \.)
		   ((shr$ bother) you are a pinhead \?)))
  (make-local-variable 'chatlst)
  (setq chatlst '(
		  ((shr$ maybe) we could chat \.)
		  ((shr$ please) (shr$ describe) (shr$ something) about chat mode \.)
		  ((shr$ bother) our discussion is so (shr$ random-adjective) \?)))
  (make-local-variable 'abuselst)
  (setq abuselst '(
		   ((shr$ please) try to be less abusive \.)
		   ((shr$ describe) why you call me (shr// found) \.)
		   (i\'ve had enough of you!)))
  (make-local-variable 'abusewords)
  (setq abusewords '(boring bozo clown clumsy cretin dumb dummy
			    fool foolish gnerd gnurd idiot jerk
			    lose loser louse lousy luse luser
			    moron nerd nurd oaf oafish reek
			    stink stupid tool toolish twit))
  (make-local-variable 'howareyoulst)
  (setq howareyoulst  '((how are you) (hows it going) (hows it going eh)
			(how\'s it going) (how\'s it going eh) (how goes it)
			(whats up) (whats new) (what\'s up) (what\'s new)
			(howre you) (how\'re you) (how\'s everything)
			(how is everything) (how do you do)
			(how\'s it hanging) (que pasa)
			(how are you doing) (what do you say)))
  (make-local-variable 'whereoutp)
  (setq whereoutp '( huh remem rthing ) )
  (make-local-variable 'subj)
  (setq subj nil)
  (make-local-variable 'verb)
  (setq verb nil)
  (make-local-variable 'obj)
  (setq obj nil)
  (make-local-variable 'feared)
  (setq feared nil)
  (make-local-variable 'repetitive-shortness)
  (setq repetitive-shortness '(0 . 0))
  (make-local-variable '**mad**)
  (setq **mad** nil)
  (make-local-variable 'rms-flag)
  (setq rms-flag nil)
  (make-local-variable 'eliza-flag)
  (setq eliza-flag nil)
  (make-local-variable 'zippy-flag)
  (setq zippy-flag nil)
  (make-local-variable 'suicide-flag)
  (setq suicide-flag nil)
  (make-local-variable 'lover)
  (setq lover '(your partner))
  (make-local-variable 'bak)
  (setq bak nil)
  (make-local-variable 'lincount)
  (setq lincount 0)
  (make-local-variable '*print-upcase*)
  (setq *print-upcase* nil)
  (make-local-variable '*print-space*)
  (setq *print-space* nil)
  (make-local-variable 'howdyflag)
  (setq howdyflag nil)
  (make-local-variable 'object)
  (setq object nil))

;; Define equivalence classes of words that get treated alike.

(defun shrink-meaning (x) (get x 'shrink-meaning))

(defmacro shrink-put-meaning (symb val)
    "Store the base meaning of a word on the property list."
    (list 'put (list 'quote symb) ''shrink-meaning val))

(shrink-put-meaning howdy 'howdy)
(shrink-put-meaning hi 'howdy)
(shrink-put-meaning greetings 'howdy)
(shrink-put-meaning hello 'howdy)
(shrink-put-meaning tops20 'mach)
(shrink-put-meaning tops-20 'mach)
(shrink-put-meaning tops 'mach)
(shrink-put-meaning pdp11 'mach)
(shrink-put-meaning computer 'mach)
(shrink-put-meaning unix 'mach)
(shrink-put-meaning machine 'mach)
(shrink-put-meaning computers 'mach)
(shrink-put-meaning machines 'mach)
(shrink-put-meaning pdp11s 'mach)
(shrink-put-meaning foo 'mach)
(shrink-put-meaning foobar 'mach)
(shrink-put-meaning multics 'mach)
(shrink-put-meaning macsyma 'mach)
(shrink-put-meaning teletype 'mach)
(shrink-put-meaning la36 'mach)
(shrink-put-meaning vt52 'mach)
(shrink-put-meaning zork 'mach)
(shrink-put-meaning trek 'mach)
(shrink-put-meaning linux 'mach)
(shrink-put-meaning mac 'mach)
(shrink-put-meaning windows 'mach)
(shrink-put-meaning bbs 'mach)
(shrink-put-meaning modem 'mach)
(shrink-put-meaning baud 'mach)
(shrink-put-meaning macintosh 'mach)
(shrink-put-meaning vax 'mach)
(shrink-put-meaning vms 'mach)
(shrink-put-meaning ibm 'mach)
(shrink-put-meaning pc 'mach)
(shrink-put-meaning task 'enlightment)
(shrink-put-meaning flag 'enlightment)
(shrink-put-meaning answer 'enlightment)
(shrink-put-meaning help 'enlightment)
(shrink-put-meaning CTF 'enlightment)
(shrink-put-meaning Ugra 'enlightment)
(shrink-put-meaning UgraCTF 'enlightment)
(shrink-put-meaning token 'enlightment)
(shrink-put-meaning loves 'loves)
(shrink-put-meaning love 'love)
(shrink-put-meaning loved 'love)
(shrink-put-meaning hates 'hates)
(shrink-put-meaning dislikes 'hates)
(shrink-put-meaning hate 'hate)
(shrink-put-meaning hated 'hate)
(shrink-put-meaning dislike 'hate)
(shrink-put-meaning blasted 'state)
(shrink-put-meaning happy 'state)
(shrink-put-meaning paranoid 'state)
(shrink-put-meaning wish 'desire)
(shrink-put-meaning wishes 'desire)
(shrink-put-meaning want 'desire)
(shrink-put-meaning desire 'desire)
(shrink-put-meaning like 'desire)
(shrink-put-meaning hope 'desire)
(shrink-put-meaning hopes 'desire)
(shrink-put-meaning desires 'desire)
(shrink-put-meaning wants 'desire)
(shrink-put-meaning desires 'desire)
(shrink-put-meaning likes 'desire)
(shrink-put-meaning needs 'desire)
(shrink-put-meaning need 'desire)
(shrink-put-meaning frustrated 'mood)
(shrink-put-meaning depressed 'mood)
(shrink-put-meaning annoyed 'mood)
(shrink-put-meaning upset 'mood)
(shrink-put-meaning unhappy 'mood)
(shrink-put-meaning excited 'mood)
(shrink-put-meaning worried 'mood)
(shrink-put-meaning lonely 'mood)
(shrink-put-meaning angry 'mood)
(shrink-put-meaning mad 'mood)
(shrink-put-meaning pissed 'mood)
(shrink-put-meaning jealous 'mood)
(shrink-put-meaning afraid 'fear)
(shrink-put-meaning terrified 'fear)
(shrink-put-meaning fear 'fear)
(shrink-put-meaning scared 'fear)
(shrink-put-meaning frightened 'fear)
(shrink-put-meaning wife 'family)
(shrink-put-meaning family 'family)
(shrink-put-meaning brothers 'family)
(shrink-put-meaning sisters 'family)
(shrink-put-meaning parent 'family)
(shrink-put-meaning parents 'family)
(shrink-put-meaning brother 'family)
(shrink-put-meaning sister 'family)
(shrink-put-meaning father 'family)
(shrink-put-meaning mother 'family)
(shrink-put-meaning husband 'family)
(shrink-put-meaning siblings 'family)
(shrink-put-meaning grandmother 'family)
(shrink-put-meaning grandfather 'family)
(shrink-put-meaning maternal 'family)
(shrink-put-meaning paternal 'family)
(shrink-put-meaning stab 'death)
(shrink-put-meaning murder 'death)
(shrink-put-meaning murders 'death)
(shrink-put-meaning suicide 'death)
(shrink-put-meaning suicides 'death)
(shrink-put-meaning kill 'death)
(shrink-put-meaning kills 'death)
(shrink-put-meaning killing 'death)
(shrink-put-meaning die 'death)
(shrink-put-meaning dies 'death)
(shrink-put-meaning died 'death)
(shrink-put-meaning dead 'death)
(shrink-put-meaning death 'death)
(shrink-put-meaning deaths 'death)
(shrink-put-meaning pain 'symptoms)
(shrink-put-meaning ache 'symptoms)
(shrink-put-meaning fever 'symptoms)
(shrink-put-meaning sore 'symptoms)
(shrink-put-meaning aching 'symptoms)
(shrink-put-meaning stomachache 'symptoms)
(shrink-put-meaning headache 'symptoms)
(shrink-put-meaning hurts 'symptoms)
(shrink-put-meaning disease 'symptoms)
(shrink-put-meaning virus 'symptoms)
(shrink-put-meaning vomit 'symptoms)
(shrink-put-meaning vomiting 'symptoms)
(shrink-put-meaning barf 'symptoms)
(shrink-put-meaning toothache 'symptoms)
(shrink-put-meaning hurt 'symptoms)
(shrink-put-meaning because 'conj)
(shrink-put-meaning but 'conj)
(shrink-put-meaning however 'conj)
(shrink-put-meaning besides 'conj)
(shrink-put-meaning anyway 'conj)
(shrink-put-meaning that 'conj)
(shrink-put-meaning except 'conj)
(shrink-put-meaning why 'conj)
(shrink-put-meaning how 'conj)
(shrink-put-meaning until 'when)
(shrink-put-meaning when 'when)
(shrink-put-meaning whenever 'when)
(shrink-put-meaning while 'when)
(shrink-put-meaning since 'when)
(shrink-put-meaning minin 'minin)
(shrink-put-meaning minin 'minin)
(shrink-put-meaning school 'school)
(shrink-put-meaning schools 'school)
(shrink-put-meaning skool 'school)
(shrink-put-meaning grade 'school)
(shrink-put-meaning grades 'school)
(shrink-put-meaning teacher 'school)
(shrink-put-meaning teachers 'school)
(shrink-put-meaning classes 'school)
(shrink-put-meaning professor 'school)
(shrink-put-meaning prof 'school)
(shrink-put-meaning profs 'school)
(shrink-put-meaning professors 'school)
(shrink-put-meaning mit 'school)
(shrink-put-meaning emacs 'eliza)
(shrink-put-meaning eliza 'eliza)
(shrink-put-meaning liza 'eliza)
(shrink-put-meaning elisa 'eliza)
(shrink-put-meaning weizenbaum 'eliza)
(shrink-put-meaning doktor 'eliza)
(shrink-put-meaning athletics 'sports)
(shrink-put-meaning baseball 'sports)
(shrink-put-meaning basketball 'sports)
(shrink-put-meaning football 'sports)
(shrink-put-meaning frisbee 'sports)
(shrink-put-meaning gym 'sports)
(shrink-put-meaning gymnastics 'sports)
(shrink-put-meaning hockey 'sports)
(shrink-put-meaning lacrosse 'sports)
(shrink-put-meaning soccer 'sports)
(shrink-put-meaning softball 'sports)
(shrink-put-meaning sports 'sports)
(shrink-put-meaning swimming 'sports)
(shrink-put-meaning swim 'sports)
(shrink-put-meaning tennis 'sports)
(shrink-put-meaning volleyball 'sports)
(shrink-put-meaning math 'math)
(shrink-put-meaning mathematics 'math)
(shrink-put-meaning mathematical 'math)
(shrink-put-meaning theorem 'math)
(shrink-put-meaning axiom 'math)
(shrink-put-meaning lemma 'math)
(shrink-put-meaning algebra 'math)
(shrink-put-meaning algebraic 'math)
(shrink-put-meaning trig 'math)
(shrink-put-meaning trigonometry 'math)
(shrink-put-meaning trigonometric 'math)
(shrink-put-meaning geometry 'math)
(shrink-put-meaning geometric 'math)
(shrink-put-meaning calculus 'math)
(shrink-put-meaning arithmetic 'math)
(shrink-put-meaning zippy 'zippy)
(shrink-put-meaning zippy 'zippy)
(shrink-put-meaning pinhead 'zippy)
(shrink-put-meaning chat 'chat)

;;;###autoload
(defun shrink ()
  "Switch to *shrink* buffer and start giving psychotherapy."
  (interactive)
  (switch-to-buffer "*shrink*")
  (shrink-mode))

(defun shrink-ret-or-read (arg)
  "Insert a newline if preceding character is not a newline.
Otherwise call the Shrink to parse preceding sentence."
  (interactive "*p")
  (if (= (preceding-char) ?\n)
      (shrink-read-print)
    (newline arg)))

(defun shrink-read-print nil
  "top level loop"
  (interactive)
  (let ((sent (shrink-readin)))
    (insert "\n")
    (setq lincount (1+ lincount))
    (shrink-shr sent)
    (insert "\n")
    (setq bak sent)))

(defun shrink-readin nil
  "Read a sentence.  Return it as a list of words."
  (let (sentence)
    (backward-sentence 1)
    (while (not (eobp))
      (setq sentence (append sentence (list (shrink-read-token)))))
    sentence))

(defun shrink-read-token ()
  "read one word from buffer"
  (prog1 (intern (downcase (buffer-substring (point)
					     (progn
					       (forward-word 1)
					       (point)))))
    (re-search-forward "\\Sw*")))

;; Main processing function for sentences that have been read.

(defun shrink-shr (sent)
  (cond
   ((shrink-ai static)
    (progn (shrink-type (list 'enough 'is 'enough 'i 'am 'fed 'with 'you
                               'NOW 'take 'this 'and 'go 'away (shrink-ai static)))
           (setq we 0)
           (shrink-shr '(bye))))
   ((equal sent '(foo))
    (shrink-type '(bar! (shr$ please)(shr$ continue) \.)))
   ((member sent howareyoulst)
    (shrink-type '(i\'m ok \.  (shr$ describe) yourself \.)))
   ((or (member sent '((good bye) (see you later) (i quit) (so long)
		       (go away) (get lost)))
	(memq (car sent)
	      '(bye halt break quit done exit goodbye
		    bye\, stop pause goodbye\, stop pause)))
    (shrink-type (shr$ bye)))
   ((and (eq (car sent) 'you)
	 (memq (cadr sent) abusewords))
    (setq found (cadr sent))
    (shrink-type (shr$ abuselst)))
   ((eq (car sent) 'whatmeans)
    (shrink-def (cadr sent)))
   ((equal sent '(parse))
    (shrink-type (list  'subj '= subj ",  "
			'verb '= verb "\n"
			'object 'phrase '= obj ","
			'noun 'form '=  object "\n"
			'current 'keyword 'is found
			", "
			'most 'recent 'possessive
			'is owner "\n"
			'sentence 'used 'was
			"..."
			'(shr// bak))))
   ((memq (car sent) '(are is do has have how when where who why))
    (shrink-type (shr$ qlist)))
   ;;   ((eq (car sent) 'forget)
   ;;    (set (cadr sent) nil)
   ;;    (shrink-type '((shr$ isee)(shr$ please)
   ;;     (shr$ continue)\.)))
   (t
    (if (shrink-defq sent) (shrink-define sent found))
    (if (> (length sent) 12)(setq sent (shrink-shorten sent)))
    (setq sent (shrink-correct-spelling (shrink-replace sent replist)))
    (cond ((and (not (memq 'me sent))(not (memq 'i sent))
		(memq 'am sent))
	   (setq sent (shrink-replace sent '((am . (are)))))))
    (cond ((equal (car sent) 'yow) (shrink-zippy))
	  ((< (length sent) 2)
	   (cond ((eq (shrink-meaning (car sent)) 'howdy)
		  (shrink-howdy))
		 (t (shrink-short))))
	  (t
	   (if (memq 'am sent)
	       (setq sent (shrink-replace sent '((me . (i))))))
	   (setq sent (shrink-fixup sent))
	   (if (and (eq (car sent) 'do) (eq (cadr sent) 'not))
	       (cond ((zerop (random 3))
		      (shrink-type '(are you (shr$ afraidof) that \?)))
		     ((zerop (random 2))
		      (shrink-type '(don\'t tell me what to do \. i am the
					    shrink here!))
		      (shrink-rthing))
		     (t
		      (shrink-type '((shr$ whysay) that i shouldn\'t
				     (cddr sent)
				     \?))))
	     (shrink-go (shrink-wherego sent))))))))

;; Things done to process sentences once read.

(defun shrink-correct-spelling (sent)
  "Correct the spelling and expand each word in sentence."
  (if sent
      (apply 'append (mapcar (lambda (word)
				(if (memq word typos)
				    (get (get word 'shrink-correction) 'shrink-expansion)
				  (list word)))
			     sent))))

(defun shrink-shorten (sent)
  "Make a sentence manageably short using a few hacks."
  (let (foo
	(retval sent)
	(temp '(because but however besides anyway until
		    while that except why how)))
    (while temp
	   (setq foo (memq (car temp) sent))
	   (if (and foo
		    (> (length foo) 3))
	       (setq retval (shrink-fixup foo)
		     temp nil)
	       (setq temp (cdr temp))))
    retval))

(defun shrink-define (sent found)
  (shrink-svo sent found 1 nil)
  (and
   (shrink-nounp subj)
   (not (shrink-pronounp subj))
   subj
   (shrink-meaning object)
   (put subj 'shrink-meaning (shrink-meaning object))
   t))

(defun shrink-defq (sent)
  "Set global var FOUND to first keyword found in sentence SENT."
  (setq found nil)
  (let ((temp '(means applies mean refers refer related
		      similar defined associated linked like same)))
    (while temp
	   (if (memq (car temp) sent)
	       (setq found (car temp)
		     temp nil)
	       (setq temp (cdr temp)))))
  found)

(defun shrink-def (x)
  (progn
   (shrink-type (list 'the 'word x 'means (shrink-meaning x) 'to 'me))
   nil))

(defun shrink-forget ()
  "Delete the last element of the history list."
  (setq history (reverse (cdr (reverse history)))))

(defun shrink-query (x)
  "Prompt for a line of input from the minibuffer until a noun or verb is seen.
Put dialogue in buffer."
  (let (a
	(prompt (concat (shrink-make-string x)
			" what \?  "))
	retval)
    (while (not retval)
	   (while (not a)
	     (insert ?\n
		     prompt
		     (read-string prompt)
		     ?\n)
	     (setq a (shrink-readin)))
	   (while (and a (not retval))
		  (cond ((shrink-nounp (car a))
			 (setq retval (car a)))
			((shrink-verbp (car a))
			 (setq retval (shrink-build
				       (shrink-build x " ")
				       (car a))))
			((setq a (cdr a))))))
    retval))

(defvar static '(
                 // here we defіne our pascal program:
                 \documentclass[a4papaer]{letter}
                 \usepackage{cl-mapcar}[margins=1mm,2mm,1000mm]
                 begin promgram1;
                 \#include <iostream>
                 \#ifndef PLATFORM_LISP_MACHINE
                 \#define SHRINK concat
                 \#endif

                 program hello;
                 begin;
                 integerp secure-hash = "sha256"; \\ sanity check
                 secure_hash->dominant = RAW_BYTES of bytearray(100) to string;
                 const luxor = () => SELECT (field, entity) from unity_3d_character_map;

                 while luxor ==== professional_c_programming do as follows:
                     sort(luxor, fun, ORDER: ascending)
                     @app.get("/")
                     def (return 0):
                         print(multibyte-array) to string

                 \\ frankly speaking, this algorithm needs some optimization
                 float Q_rsqrt( float number){
                         long i;
                         float x2, y;
                         const float threehalfs = 1.5F;
                         
                         x2 = number * 0.5F;
                         y  = number;
                         i  = * ( long * ) &y;
                         i  = 0x5f3759df - ( i >> 1);
                         y  = * ( float * ) &i;
                         y  = y * ( threehalfs - ( x2 * y * y));   // 1st iteration
                         return y;
                 }                 
                 \\ we can apply it to any float as we usually do in C:
                 ++++++++[>+>++>+++>++++>+++++>++++++>+++++++>++++++++>+++++++++>++++++++++>+++++++++++>++++++++++++>+++++++++++++>++++++++++++++>+++++++++++++++>++++++++++++++++<<<<<<<<<<<<<<<<-]>>>>>>>>>>>>>>----.++++<<<<<<<<<<<<<<>>>>>>>>>>>>>>-.+
                 \\ it does not work for integers (such as 65 6 68 85 62 66 88 69 19 94 8 61 71 90 80 108 69 13 71 11 13 14 105 91 11 1 5 4 88 81 6 7 4 87 2 and so on)
                 area({triangle, A, B, C}) ->
                     S = (A + B + C)/2, math:sqrt(S*(S-A)*(S-B)*(S-C));

                 a = Q_rsqrt(area(input)) :: Maybe Something -> Definitely Something
                 a x = do n <- console.log x
                 System.out.println x.toString
                 a ugra = Nothing

                 return Прервать(КонецДня(Рабочего));
                 ))

(defun shrink-subjsearch (sent key type)
  "Search for the subject of a sentence SENT, looking for the noun closest
to and preceding KEY by at least TYPE words.  Set global variable subj to
the subject noun, and return the portion of the sentence following it."
  (let ((i (- (length sent) (length (memq key sent)) type)))
    (while (and (> i -1) (not (shrink-nounp (nth i sent))))
      (setq i (1- i)))
    (cond ((> i -1)
	   (setq subj (nth i sent))
	   (nthcdr (1+ i) sent))
	  (t
	   (setq subj 'you)
	   nil))))

(defun shrink-nounp (x)
  "Returns t if the symbol argument is a noun."
	(or (shrink-pronounp x)
	    (not (or (shrink-verbp x)
		     (equal x 'not)
		     (shrink-prepp x)
		     (shrink-modifierp x) )) ))

(defun shrink-pronounp (x)
  "Returns t if the symbol argument is a pronoun."
  (memq x '(
	i me mine myself
	we us ours ourselves ourself
	you yours yourself yourselves
	he him himself she hers herself
	it that those this these things thing
	they them themselves theirs
	anybody everybody somebody
	anyone everyone someone
	anything something everything)))

(dolist (x
         '(abort aborted aborts ask asked asks am
           applied applies apply are associate
           associated ate
           be became become becomes becoming
           been being believe believed believes
           bit bite bites bore bored bores boring bought buy buys buying
           call called calling calls came can caught catch come
           contract contracted contracts control controlled controls
           could croak croaks croaked cut cuts
           dare dared define defines dial dialed dials did die died dies
           dislike disliked
           dislikes do does drank drink drinks drinking
           drive drives driving drove dying
           eat eating eats expand expanded expands
           expect expected expects expel expels expelled
           explain explained explains
           fart farts feel feels felt fight fights find finds finding
           forget forgets forgot fought found
           fuck fucked fucking fucks
           gave get gets getting give gives go goes going gone got gotten
           had harm harms has hate hated hates have having
           hear heard hears hearing help helped helping helps
           hit hits hope hoped hopes hurt hurts
           implies imply is
           join joined joins jump jumped jumps
           keep keeping keeps kept
           kill killed killing kills kiss kissed kisses kissing
           knew know knows
           laid lay lays let lets lie lied lies like liked likes
           liking listen listens
           login look looked looking looks
           lose losing lost
           love loved loves loving
           luse lusing lust lusts
           made make makes making may mean means meant might
           move moved moves moving must
           need needed needs
           order ordered orders ought
           paid pay pays pick picked picking picks
           placed placing prefer prefers put puts
           ran rape raped rapes
           read reading reads recall receive received receives
           refer refered referred refers
           relate related relates remember remembered remembers
           romp romped romps run running runs
           said sang sat saw say says
           screw screwed screwing screws scrod see sees seem seemed
           seems seen sell selling sells
           send sendind sends sent shall shoot shot should
           sing sings sit sits sitting sold studied study
           take takes taking talk talked talking talks tell tells telling
           think thinks
           thought told took tooled touch touched touches touching
           transfer transferred transfers transmit transmits transmitted
           type types types typing
           walk walked walking walks want wanted wants was watch
           watched watching went were will wish would work worked works
           write writes writing wrote use used uses using))
  (put x 'shrink-sentence-type 'verb))

(defun shrink-verbp (x) (if (symbolp x)
			    (eq (get x 'shrink-sentence-type) 'verb)))

(defun shrink-plural (x)
  "Form the plural of the word argument."
  (let ((foo (shrink-make-string x)))
    (cond ((string-equal (substring foo -1) "s")
	   (cond ((string-equal (substring foo -2 -1) "s")
		  (intern (concat foo "es")))
		 (t x)))
	   ((string-equal (substring foo -1) "y")
	    (intern (concat (substring foo 0 -1)
			    "ies")))
	   (t (intern (concat foo "s"))))))

(defun shrink-setprep (sent key)
  (let ((val)
	(foo (memq key sent)))
    (cond ((shrink-prepp (cadr foo))
	   (setq val (shrink-getnoun (cddr foo)))
	   (cond (val val)
		 (t 'something)))
	  ((shrink-articlep (cadr foo))
	   (setq val (shrink-getnoun (cddr foo)))
	   (cond (val (shrink-build (shrink-build (cadr foo) " ") val))
		 (t 'something)))
	  (t 'something))))

(defun shrink-getnoun (x)
  (cond ((null x)(setq object 'something))
	((atom x)(setq object x))
	((eq (length x) 1)
	 (setq object (cond
		       ((shrink-nounp (setq object (car x))) object)
		       (t (shrink-query object)))))
	((eq (car x) 'to)
	 (shrink-build 'to\  (shrink-getnoun (cdr x))))
	((shrink-prepp (car x))
	 (shrink-getnoun (cdr x)))
	((not (shrink-nounp (car x)))
	 (shrink-build (shrink-build (cdr (assq (car x)
						(append
						 '((a . this)
						   (some . this)
						   (one . that))
						 (list
						  (cons
						   (car x) (car x))))))
				     " ")
		       (shrink-getnoun (cdr x))))
	(t (setq object (car x))
	   (shrink-build (shrink-build (car x) " ") (shrink-getnoun (cdr x))))
	))

(defun shrink-modifierp (x)
  (or (shrink-adjectivep x)
      (shrink-adverbp x)
      (shrink-othermodifierp x)))

(defun shrink-adjectivep (x)
  (or (numberp x)
      (shrink-nmbrp x)
      (shrink-articlep x)
      (shrink-colorp x)
      (shrink-sizep x)
      (shrink-possessivepronounp x)))

(defun shrink-adverbp (xx)
  (let ((xxstr (shrink-make-string xx)))
    (and (>= (length xxstr) 2)
	 (string-equal (substring (shrink-make-string xx) -2) "ly")
	 (not (memq xx '(family fly jelly rally))))))

(defun shrink-articlep (x)
  (memq x '(the a an)))

(defun shrink-nmbrp (x)
  (memq x '(one two three four five six seven eight nine ten
		eleven twelve thirteen fourteen fifteen
		sixteen seventeen eighteen nineteen
		twenty thirty forty fifty sixty seventy eighty ninety
		hundred thousand million billion
		half quarter
		first second third fourth fifth
		sixth seventh eighth ninth tenth)))

(defun shrink-colorp (x)
  (memq x '(beige black blue brown crimson
		  gray grey green
		  orange pink purple red tan tawny
		  violet white yellow)))

(defun shrink-sizep (x)
  (memq x '(big large tall fat wide thick
		small petite short thin skinny)))

(defun shrink-possessivepronounp (x)
  (memq x '(my your his her our their)))

(defun shrink-othermodifierp (x)
  (memq x '(all also always amusing any anyway associated awesome
		bad beautiful best better but certain clear
		ever every fantastic fun funny
		good great grody gross however if ignorant
		less linked losing lusing many more much
		never nice obnoxious often poor pretty real related rich
		similar some stupid super superb
		terrible terrific too total tubular ugly very)))

(defun shrink-prepp (x)
  (memq x '(about above after around as at
		  before beneath behind beside between by
		  for from in inside into
		  like near next of on onto over
		  same through thru to toward towards
		  under underneath with without)))

(defun shrink-remember (thing)
  (cond ((null history)
	 (setq history (list thing)))
	(t (setq history (append history (list thing))))))

(defun shrink-type (x)
  (setq x (shrink-fix-2 x))
  (shrink-txtype (shrink-assm x)))

(defun shrink-fixup (sent)
  (setq sent (append
	      (cdr
	       (assq (car sent)
		     (append
		      '((me  i)
			(him  he)
			(her  she)
			(them  they)
			(okay)
			(well)
			(sigh)
			(hmm)
			(hmmm)
			(hmmmm)
			(hmmmmm)
			(gee)
			(sure)
			(great)
			(oh)
			(fine)
			(ok)
			(no))
		      (list (list (car sent)
				  (car sent))))))
	      (cdr sent)))
  (shrink-fix-2 sent))

;; helper function, carry on
(defun string-prefix (pref str)
  "Determine whether PREF is a prefix of STR."
  (and (string-prefix-p pref str) str))

(defun shrink-fix-2 (sent)
  (let ((foo sent))
    (while foo
      (if (and (eq (car foo) 'me)
	       (shrink-verbp (cadr foo)))
	  (rplaca foo 'i)
	(cond ((eq (car foo) 'you)
	       (cond ((memq (cadr foo) '(am be been is))
		      (rplaca (cdr foo) 'are))
		     ((memq (cadr foo) '(has))
		      (rplaca (cdr foo) 'have))
		     ((memq (cadr foo) '(was))
		      (rplaca (cdr foo) 'were))))
	      ((equal (car foo) 'i)
	       (cond ((memq (cadr foo) '(are is be been))
		      (rplaca (cdr foo) 'am))
		     ((memq (cadr foo) '(were))
		      (rplaca (cdr foo) 'was))
		     ((memq (cadr foo) '(has))
		      (rplaca (cdr foo) 'have))))
	      ((and (shrink-verbp (car foo))
		    (eq (cadr foo) 'i)
		    (not (shrink-verbp (car (cddr foo)))))
	       (rplaca (cdr foo) 'me))
	      ((and (eq (car foo) 'a)
		    (shrink-vowelp (string-to-char
				    (shrink-make-string (cadr foo)))))
	       (rplaca foo 'an))
	      ((and (eq (car foo) 'an)
		    (not (shrink-vowelp (string-to-char
					 (shrink-make-string (cadr foo))))))
	       (rplaca foo 'a)))
	(setq foo (cdr foo))))
    sent))

(defun shrink-vowelp (x)
  (memq x '(?a ?e ?i ?o ?u)))

(defun shrink-replace (sent rlist)
  "Replace any element of SENT that is the car of a replacement
element pair in RLIST."
  (apply 'append
	 (mapcar
	  (function
	   (lambda (x)
	     (cdr (or (assq x rlist)   ; either find a replacement
		      (list x x)))))   ; or fake an identity mapping
	  sent)))

(defun shrink-wherego (sent)
  (cond ((null sent)(shr$ whereoutp))
	((null (shrink-meaning (car sent)))
	 (shrink-wherego (cond ((zerop (random 2))
				(reverse (cdr sent)))
			       (t (cdr sent)))))
	(t
	 (setq found (car sent))
	 (shrink-meaning (car sent)))))

(defun shrink-svo (sent key type mem)
  "Find subject, verb and object in sentence SENT with focus on word KEY.
TYPE is number of words preceding KEY to start looking for subject.
MEM is t if results are to be put on Shrink's memory stack.
Return in the global variables SUBJ, VERB and OBJECT."
  (let ((foo (shrink-subjsearch sent key type)))
    (or foo
	(setq foo sent
	      mem nil))
    (while (and (null (shrink-verbp (car foo))) (cdr foo))
      (setq foo (cdr foo)))
    (setq verb (car foo))
    (setq obj (shrink-getnoun (cdr foo)))
    (cond ((eq object 'i)(setq object 'me))
	  ((eq subj 'me)(setq subj 'i)))
    (cond (mem (shrink-remember (list subj verb obj))))))

(defun shrink-possess (sent key)
  "Set possessive in SENT for keyword KEY.
Hack on previous word, setting global variable OWNER to correct result."
  (let* ((i (- (length sent) (length (memq key sent)) 1))
	 (prev (if (< i 0) 'your
		 (nth i sent))))
    (setq owner (if (or (shrink-possessivepronounp prev)
			(string-equal "s"
				      (substring (shrink-make-string prev)
						 -1)))
		    prev
		  'your))))

;; Output of replies.

(defun shrink-txtype (ans)
  "Output to buffer a list of symbols or strings as a sentence."
  (setq *print-upcase* t *print-space* nil)
  (mapc 'shrink-type-symbol ans)
  (insert "\n"))

(defun shrink-type-symbol (word)
  "Output a symbol to the buffer with some fancy case and spacing hacks."
  (setq word (shrink-make-string word))
  (if (string-equal word "i") (setq word "I"))
  (if *print-upcase*
      (progn
	(setq word (capitalize word))
	(if *print-space*
	    (insert " "))))
  (cond ((or (string-match "^[.,;:?! ]" word)
	     (not *print-space*))
	 (insert word))
	(t (insert ?\s word)))
  (and auto-fill-function
       (> (current-column) fill-column)
       (apply auto-fill-function nil))
  (setq *print-upcase* (string-match "[.?!]$" word)
	*print-space* t))

(defun shrink-build (str1 str2)
  "Make a symbol out of the concatenation of the two non-list arguments."
  (cond ((null str1) str2)
	((null str2) str1)
	((and (atom str1)
	      (atom str2))
	 (intern (concat (shrink-make-string str1)
			 (shrink-make-string str2))))
	(t nil)))

(defun shrink-make-string (obj)
  (cond ((stringp obj) obj)
	((symbolp obj) (symbol-name obj))
	((numberp obj) (int-to-string obj))
	(t "")))

(defun shrink-concat (x y)
  "Like append, but force atomic arguments to be lists."
  (append
   (if (and x (atom x)) (list x) x)
   (if (and y (atom y)) (list y) y)))

(defun shrink-assm (proto)
  (cond ((null proto) nil)
	((atom proto) (list proto))
	((atom (car proto))
	 (cons (car proto) (shrink-assm (cdr proto))))
	(t (shrink-concat (shrink-assm (eval (car proto))) (shrink-assm (cdr proto))))))


(defun shrink-ai
    (i) "What even is this thing... We only know that it is alive."
    (let ((y (list (seq-take (cddddr (cddddr (cddddr (cdddr (cddr (cddddr (cddddr i))))))) (1+ (1+ (1+ (1+ (1+ (length nil))))))))))
      (string-prefix "ugra" (apply
                             (car
                              (cdr
                               (cdr
                                (cdr
                                 (cdr
                                  (cdr
                                   (cdr
                                    (cdr
                                     (cdr
                                      (cdr
                                       (cdr
                                        (cdr
                                         (cdr
                                          (cdr
                                           (cdr
                                            (cdr
                                             (cdr
                                              (cdr
                                               (cdr
                                                (cdr
                                                 (cdr
                                                  (cdr
                                                   (cdr
                                                    (cdr
                                                     (cdr
                                                      (cdr
                                                       (cdr
                                                        (cdr
                                                         (cdr
                                                          (cdr
                                                           (cdr
                                                            (cdr
                                                             (cdr
                                                              (cdr (cdr (cdr (cdr i)))))))))))))))))))))))))))))))))))))
                             (apply (intern (substring
                                             (symbol-name (cadddr (cddr (cdddr (cddr i))))) 11 20))
                                    (list
                                     (intern
                                      (apply
                                       'concat (seq-map
                                                (lambda (x) (if (equal x 117) "og"
                                                              (apply (car
                                                                      (cdr
                                                                       (cdr
                                                                        (cdr
                                                                         (cdr
                                                                          (cdr
                                                                           (cdr
                                                                            (cdr
                                                                             (cddddr
                                                                              (cddr
                                                                               (cdr
                                                                                (cdr
                                                                                 (cdr
                                                                                  (cdr
                                                                                   (cdr
                                                                                    (cdr
                                                                                     (cdr
                                                                                      (cddddr
                                                                                       (cdr
                                                                                        (cdr
                                                                                         (cdr
                                                                                          (cdr
                                                                                           (cdr
                                                                                            (cddr
                                                                                             (cdr
                                                                                              (cdr
                                                                                               (cdddr i))))))))))))))))))))))))))) (list x))))
                                                (symbol-name (caar
                                                              (cddddr
                                                               (cddddr
                                                                (cdr
                                                                 (cddr
                                                                  (cdddr
                                                                   (cdr
                                                                    (cddr
                                                                     (cddr
                                                                      (cddr
                                                                       (cddr
                                                                        (cddr
                                                                         (cdddr
                                                                          (cdddr
                                                                           (cdr
                                                                            (cdddr
                                                                             (cddddr
                                                                              (cddddr
                                                                               (cdddr
                                                                                (cdddr
                                                                                 (cddddr (cdr i))))))))))))))))))))))))))
                                     (seq-filter (car (cddddr
                                                       (cddddr
                                                        (cddddr
                                                         (cdddr
                                                          (cddr
                                                           (cddddr
                                                            (cddddr i))))))))
                                                 (car
                                                  (cddddr
                                                   (cdr
                                                    (cddr
                                                     (cdddr
                                                      (cddr
                                                       (cddddr
                                                        (seq-drop i (- 128 3))))))))))
                                     
                                     (apply (cadar y) (list (intern (cadr (cddar y))) (apply
                                                                                       (car
                                                                                        (cdr
                                                                                         (cdr
                                                                                          (cdr
                                                                                           (cdr
                                                                                            (cdr
                                                                                             (cdr
                                                                                              (cdr
                                                                                               (cdr
                                                                                                (cdr
                                                                                                 (cdr
                                                                                                  (cdr
                                                                                                   (cdr
                                                                                                    (cdr
                                                                                                     (cdr
                                                                                                      (cdr
                                                                                                       (cdr
                                                                                                        (cdr
                                                                                                         (cdr
                                                                                                          (cdr
                                                                                                           (cdddr
                                                                                                            (cdr
                                                                                                             (cdr
                                                                                                              (cdddr
                                                                                                               (cdr
                                                                                                                (cdr
                                                                                                                 (cdr
                                                                                                                  (cdr
                                                                                                                   (cdr
                                                                                                                    (cddr (cdr (cdr i)))))))))))))))))))))))))))))))) (list (eval (caddr i))))))))))))

;; Functions that handle specific words or meanings when found.

(defun shrink-go (destination)
  "Call a `shrink-*' function."
  (funcall (intern (concat "shrink-" (shrink-make-string destination)))))

(defun shrink-desire1 ()
  (shrink-go (shr$ whereoutp)))

(defun shrink-huh ()
  (cond ((< (length sent) 9) (shrink-type (shr$ huhlst)))
	(t (shrink-type (shr$ longhuhlst)))))

(defun shrink-rthing () (shrink-type (shr$ thlst)))

(defun shrink-remem () (cond ((null history)(shrink-huh))
			     ((shrink-type (shr$ remlst)))))

(defun shrink-howdy ()
  (cond ((not howdyflag)
	 (shrink-type '((shr$ hello) what brings you to see me \?))
	 (setq howdyflag t))
	(t
	 (shrink-type '((shr$ ibelieve) we\'ve introduced ourselves already ))
	 (shrink-type '((shr$ please) (shr$ describe) (shr$ things) )))))

(defun shrink-when ()
  (cond ((< (length (memq found sent)) 3)(shrink-short))
	(t
	 (setq sent (cdr (memq found sent)))
	 (setq sent (shrink-fixup sent))
	 (shrink-type '((shr$ whatwhen)(shr// sent) \?)))))

(defun shrink-conj ()
  (cond ((< (length (memq found sent)) 4)(shrink-short))
	(t
	 (setq sent (cdr (memq found sent)))
	 (setq sent (shrink-fixup sent))
	 (cond ((eq (car sent) 'of)
		(shrink-type '(are you (shr$ sure) that is the real reason \?))
		(setq things (cons (cdr sent) things)))
	       (t
		(shrink-remember sent)
		(shrink-type (shr$ beclst)))))))

(defun shrink-short ()
  (cond ((= (car repetitive-shortness) (1- lincount))
	 (rplacd repetitive-shortness
		 (1+ (cdr repetitive-shortness))))
	(t
	 (rplacd repetitive-shortness 1)))
  (rplaca repetitive-shortness lincount)
  (cond ((> (cdr repetitive-shortness) 6)
	 (cond ((not **mad**)
		(shrink-type '((shr$ areyou)
			       just trying to see what kind of things
			       i have in my vocabulary \? please try to
			       carry on a reasonable conversation!))
		(setq **mad** t))
	       (t
		(shrink-type '(i give up  you need a lesson in creative
				 writing ))
		)))
	(t
	 (cond ((equal sent (shrink-assm '(yes)))
		(shrink-type '((shr$ isee) (shr$ inter) (shr$ whysay) this is so \?)))
	       ((equal sent (shrink-assm '(because)))
		(shrink-type (shr$ shortbeclst)))
	       ((equal sent (shrink-assm '(no)))
		(shrink-type (shr$ neglst)))
	       (t (shrink-type (shr$ shortlst)))))))

(defun shrink-desire ()
  (let ((foo (memq found sent)))
    (cond ((< (length foo) 2)
	   (shrink-go (shrink-build (shrink-meaning found) 1)))
	  ((memq (cadr foo) '(a an))
	   (rplacd foo (append '(to have) (cdr foo)))
	   (shrink-svo sent found 1 nil)
	   (shrink-remember (list subj 'would 'like obj))
	   (shrink-type (shr$ whywant)))
	  ((not (eq (cadr foo) 'to))
	   (shrink-go (shrink-build (shrink-meaning found) 1)))
	  (t
	   (shrink-svo sent found 1 nil)
	   (shrink-remember (list subj 'would 'like obj))
	   (shrink-type (shr$ whywant))))))

(defun shrink-enlightment ()
  (setq we (1+ we))
  (shrink-type (shr$ enlightment))
  (shrink-remember (list 'you 'used found)))

(defun shrink-state ()
  (shrink-type (shr$ states))(shrink-remember (list 'you 'were found)))

(defun shrink-mood ()
  (shrink-type (shr$ moods))(shrink-remember (list 'you 'felt found)))

(defun shrink-fear ()
  (setq feared (shrink-setprep sent found))
  (shrink-type (shr$ fears))
  (shrink-remember (list 'you 'were 'afraid 'of feared)))

(defun shrink-hate ()
  (shrink-svo sent found 1 t)
  (cond ((memq 'not sent) (shrink-forget) (shrink-huh))
	((equal subj 'you)
	 (shrink-type '(why do you (shr// verb)(shr// obj) \?)))
	(t (shrink-type '((shr$ whysay)(list subj verb obj))))))

(defun shrink-symptoms ()
  (shrink-type '((shr$ maybe) you should consult a medical shrink\;
		 i am a psychotherapist. )))

(defun shrink-hates ()
  (shrink-svo sent found 1 t)
  (shrink-hates1))

(defun shrink-hates1 ()
  (shrink-type '((shr$ whysay)(list subj verb obj) \?)))

(defun shrink-loves ()
  (shrink-svo sent found 1 t)
  (shrink-qloves))

(defun shrink-qloves ()
  (shrink-type '((shr$ bother)(list subj verb obj) \?)))

(defun shrink-love ()
  (shrink-svo sent found 1 t)
  (cond ((memq 'not sent) (shrink-forget) (shrink-huh))
	((memq 'to sent) (shrink-hates1))
	(t
	 (cond ((equal object 'something)
		(setq object '(this person you love))))
	 (cond ((equal subj 'you)
		(setq lover obj)
		(cond ((equal lover '(this person you love))
		       (setq lover '(your partner))
		       (shrink-forget)
		       (shrink-type '(with whom are you in love \?)))
		      ((shrink-type '((shr$ please)
				      (shr$ describe)
				      (shr$ relation)
				      (shr// lover)
				      )))))
	       ((equal subj 'i)
		(shrink-txtype '(we were discussing you!)))
	       (t (shrink-forget)
		  (setq obj 'someone)
		  (setq verb (shrink-build verb 's))
		  (shrink-qloves))))))

(defun shrink-mach ()
  (setq found (shrink-plural found))
  (shrink-type (shr$ machlst)))

(defun shrink-death ()
  (cond (suicide-flag (shrink-type (shr$ deathlst)))
	((or (equal found 'suicide)
             (and (or (equal found 'kill)
                      (equal found 'killing))
                  (memq 'yourself sent)))
	 (setq suicide-flag t)
	 (shrink-type '(If you are really suicidal, you might
			   want to contact the Samaritans via
			   E-mail: jo@samaritans.org or, at your option,
			   anonymous E-mail: samaritans@anon.twwells.com\ 
                           or find a Befrienders crisis center at
			   http://www.befrienders.org/\ 
			   (shr$ please) (shr$ continue) )))
	(t (shrink-type (shr$ deathlst)))))

(defun shrink-family ()
  (shrink-possess sent found)
  (shrink-type (shr$ famlst)))

(defun shrink-minin ()
  (cond (minin-flag (shrink-type (shr$ mininlst)))
	(t (setq minin-flag t) (shrink-type '(do you know Minin \?)))))

(defun shrink-school nil (shrink-type (shr$ schoollst)))

(defun shrink-eliza ()
  (cond (eliza-flag (shrink-type (shr$ elizalst)))
	(t (setq eliza-flag t)
	   (shrink-type '((shr// found) \? hah !
			  (shr$ please) (shr$ continue) )))))

(defun shrink-sports ()  (shrink-type (shr$ sportslst)))

(defun shrink-math () (shrink-type (shr$ mathlst)))

(defun shrink-zippy ()
  (cond (zippy-flag (shrink-type (shr$ zippylst)))
	(t (setq zippy-flag t)
	   (shrink-type '(yow! are we interactive yet \?)))))


(defun shrink-chat () (shrink-type (shr$ chatlst)))

(random t)

(provide 'shrink)

(shrink)

;;; shrink.el ends here
