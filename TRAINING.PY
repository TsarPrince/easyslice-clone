# total word count: 150-600 words
import json

example_stories = [
  # story 1
  {
    "title": "Can every single one of us surround our whole planet?",
    "total_word_count": 190,
    "clips": [
      # clip 1: If every single one of us ... That is a sir cool. (9.1 - 84.62)
      {
        "clip": 1,
        "sentence": "If every single one of us held hands together in a chain of unity around Earth, would there be enough of us to go all the way around the planet? There are about 7 .5 billion of us, and that's a lot, but remember that that many human bodies thrown together into one big pile would barely fill the Grand Canyon. This is all of us in one place. The physical bulk of all living human flesh on Earth today would only make a cone about 7 ,000 people tall and 2 ,000 across. That's it. But that's a three -dimensional shape. What if we made a one -dimensional, single -file line of people each with, say, one meter of a row, and we stretched that around the planet? it. Well, we would make it all the way around and still have 99 .5 % of the human population left. If we made a circle that included everyone, the ring of people would be more than 2 .4 million kilometers in diameter, dorking the orbit of our own moon. Now that's not just a circle. That is a sir cool.",
        "start_index": 4,
        "end_index": 193,
        "word_count": 190,
      }
    ]
  },
  # story 2
  {
    "title": "What is \"rolling\" and how to design the perfect road instead of the perfect wheel!",
    "total_word_count": 182,
    "clips": [
      # clip 1: what is rolling? ... allows it to roll smoothly. (93.74000000000001 - 167.16)
      {
        "clip": 1,
        "sentence": "what is rolling? Well, rolling occurs whenever something moves with respect to something else and is always in contact with that something else and the contact points have instantaneous velocities of zero. That is, there's no slide. In mathematics, the path traced by a point on a rolling object is called a roulette. French for little wheel. The center of a disc produces a roulette that's just a smooth straight line, while rolling on one, and this is why discs are good wheels. A square, on the other hand, would be bumpy. But square centers can make straight, smooth roulette across the right surfaces. This is the principle behind square wheels, which I recently had the pleasure of enjoying at the Museum of Mathematics in New York City. Stan Wagon wrote a fantastic and famous article about wheels, which I've linked down in the description below. It's a great read. He also contributed a fantastic interactive tool to the Wolfram demonstration project that allows you to build a wheel and then find the corresponding road shape that allows it to roll smoothly.",
        "start_index": 206,
        "end_index": 387,
        "word_count": 182,
      }
    ]
  },
  # story 3
  {
    "title": "What is the fastest path to roll down to a point?",
    "total_word_count": 524,

    "clips": [
      # clip 1: let me ask you this ... cycloid satisfies, snells law, everywhere. (284.62 - 478.88)
      {
        "clip": 1,
        "sentence": "let me ask you this. With only gravity to move you, what's the fastest way to roll or slide from a point to some other point below, but not directly below? Would it be a straight line? Well, that would certainly be the shortest path. But when you fall, gravity accelerates you, and falling vertically a lot right away would mean having a higher top speed during more of the journey. And that can make up for the fact that a path like this is much longer than a straight line. But of these two considerations, accelerate quickly and don't have too long of a path, what's the optimal combination? Finding the answer, the path of least time, is called the Brachista Crone Problem. And it's been around for a while. Galileo thought the answer was a path that's just a piece of a circle. But he was wrong, there's a better one. And in 1697, Johann Bernoulli came up with the answer using a very clever approach. To see how he solved it, let's start with a similar problem. You are standing in some mud and you want to run to a ball in the street as quickly as possible. Now, a straight line would be the path of shortest distance. But if you can run on... pavement much faster than you can run in mud. The path of shortest time would be one in which you spend less time moving slowly in mud and more time on the surface you're fast on. The angle you should enter the pavement at depends on how fast you move on both surfaces. As it turns out, when the ratio between the signs of these two angles equals the ratio between your speeds across both surfaces, the resulting path will be the optimal quickest route. This is called Snell's Law. Light always obeys Snell's Law. When it changes speeds, like when it leaves a material in which it moves more slowly, like water and enters one in which it moves more quickly, like air, it always refracts according to Snell's Law. In other words, light always follows the route that is the fastest for it to take. this fact to tackle the brachista -crown problem. Light changing speed is analogous to a falling object changing speed. But of course a falling object doesn't just speed up once, its speed is always increasing, it's accelerating. To mimic this, using light, which Bernoulli knew would always show him the fastest possible route, all he had to do was add more and thinner and thinner layers in which the speed of light was faster and faster and faster. And well, what do you know? There it is. The brachista -crown curve. The path of least time. Roll down a track like this and you will beat anything rolling down any other path every time. Bernoulli was clever enough to realize that this curve can be described in another way, as a roulette. Specifically, he noticed that it was a cycloid. The path traced by a point on a circle rolling along a line. A cycloid satisfies, snows, law, everywhere.",
        "start_index": 711,
        "end_index": 1234,
        "word_count": 524,
      }
    ]
  },
  # story 4
  {
    "title": "The physical brachistochrone & it's bizzare tautochrone property",
    "total_word_count": 334,
    "clips": [
      # clip 1: let me ask you this ... but not directly below? (284.62 - 294.3)
      {
        "clip": 1,
        "sentence": "let me ask you this. With only gravity to move you, what's the fastest way to roll or slide from a point to some other point below, but not directly below?",
        "start_index": 711,
        "end_index": 741,
        "word_count": 31,
      },
      # clip 2: a cycloid provides the perfect balance ... start building. (492.44 - 510.08)
      {
        "clip": 2,
        "sentence": "a cycloid provides the perfect balance between keeping the journey distance short and picking up speed early. Now I told Adam all of this and I told him that it would be really fun to have a cycloid curve we could roll things down. And he said, clearly we should start building.",
        "start_index": 1268,
        "end_index": 1319,
        "word_count": 52,
      },
      # clip 3: Are you ready? ... slowest way to get there. (1012.34 - 1032.78)
      {
        "clip": 3,
        "sentence": "Are you ready? I'm ready. All right, I'll count us down 321 go. Here we go. 3, 2, 1. One go One two three with the state was second straight was last straight was last the shortest distance between two points was last Slowest way to get there.",
        "start_index": 2420,
        "end_index": 2467,
        "word_count": 48,
      },
      # clip 4: I'm gonna remove the straight line ... But that's boring. (1195.54 - 1242.18)
      {
        "clip": 4,
        "sentence": "I'm gonna remove the straight line guys well, so we're left with a cycle which is called a brachista -crone curve, but it also has a bizarre property where, no matter where I start an object on it. When I let go, they always reach the bottom. In the same amount of time. Wait a second. So if I start it here, the amount of time it takes for this to get to the end is the same amount of time it takes for it to get to the end from here. Yeah, and the same from right here. Well, there. Wow, okay. So starting from here, it's going to be tough because of friction. Yeah, now if you do this in software, it's perfect. But that's boring.",
        "start_index": 2868,
        "end_index": 2995,
        "word_count": 128,
      },
      # clip 5: I think the same person ... That was awesome. (1337.16 - 1365.86)
      {
        "clip": 5,
        "sentence": "I think the same person should release them because then time it better. So here, put that one here. Okay. All right, so three different positions. This one has longer to go. Yep, this one has the shortest path. So who's gonna reach the bottom first? Okay, here we go. Let's see, if you wish it would say, the one in my, this one, we go first, ready? Yeah. Good. Pretty good. That was awesome.",
        "start_index": 3266,
        "end_index": 3340,
        "word_count": 75,
      }
    ]
  },
  # story 5
  {
    "title": "Exploring the old school Spirograph toy & the amazing Tusi couple!",
    "total_word_count": 338,
    "clips": [
      # clip 1: let's take some time to appreciate ... when bought in Oceola, Missouri. (864.92 - 989.9)
      {
        "clip": 1,
        "sentence": "let's take some time to appreciate other kinds of roulette. As mentioned before, trocoids are curves made by discs rolling on straight lines, but an epitrocoid is made when a disc rolls around the outside of a circle. Roll a disc inside a circle and what you've made is a hypo trocoid. These are the mathematical names for the curves you make when using a spyrograph toy. Notice that the holes don't lie on the circumference of the discs. Though some do come close, there's a special name for epitrocoids and hypo trocoids traced by... points on circumferences analogous to discs rolling on straight lines, they are epicycloids and hypocycloids. Now if two circles have the same radius, a point on the rolling one will touch the stationary one exactly once, always in the same spot, creating a cusp. This cute heart -shaped epicycloid is also known as a cardioid. If the rolling circle has half the larger radius, you'll get a two cusp epicycloid, the shape of which is called a nephroid, because it apparently looks like a kidney, I guess. One -third the radius gives you three cusps, one -fourth four cusps, and so on. As for hypocycloids, if the inner circles radius is one quarter of the larger, the resulting roulette curve is called an asteroid, because it looks like a star, which the ancients also thought about asteroids. One -third the radius and you've got a - deltoid, named after its resemblance to the Greek letter delta. One half the radius, and well, you get a straight line. This fun relationship is called a toocy couple. Rotational motion turned into linear motion. Follow a number of points on the rolling circle and you'll get the famous illusion where every individual point moves in a straight line, but the whole thing describes a rolling circle. Put a handle on it and you've built a tramble of arcametes, aka an ellipsograph, when used to make ellipses, aka a hillbilly entertainment center when bought in Oceola, Missouri.",
        "start_index": 2059,
        "end_index": 2396,
        "word_count": 338,
      }
    ]
  }
]

with open("in/training_data/input.json", "r") as f:
  transcript_data = json.load(f)
  for story in example_stories:
    for clip in story["clips"]:
      start = clip["start_index"]
      end = clip["end_index"]
      sentence = ' '.join([word['word'] for word in transcript_data['words'][start:end+1]])
      print(sentence)
      print()
      print()
