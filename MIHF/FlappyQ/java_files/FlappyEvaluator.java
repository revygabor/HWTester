import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;

public class FlappyEvaluator {
//    Random seedRnd = new Random();
//    int seed = seedRnd.nextInt(200);
    int seed = 33;

    public static int mapSizeX = 80;
    public static int mapSizeY = 40;
    static int size = 3;
    static int maxSpeed = 25;
    static int gapSize = 20;
    static int tubeSpeed = -2;
    static int width = 10;
    static int[] heightRange = {5, 15};

    // Environment
    class Tube {

        public int pos;
        public int height;
        boolean scored;

        Tube(int pos, int height) {
            this.pos = pos;
            this.height = height;
            this.scored = false;
        }

        void step() {
            this.pos+= tubeSpeed;
        }

        int distanceToBird(Bird bird) {
            return this.pos - bird.posX;
        }

        @Override
        public String toString() {
            return "Tube{" +
                    "pos=" + pos +
                    ", height=" + height +
                    ", scored=" + scored +
                    '}';
        }
    }
    class Bird {
        int posX, posY;
        int speed;

        Bird(int posX, int posY) {
            this.posX = posX;
            this.posY = posY;
            this.speed = 0;
        }

        void step(int force, boolean keep) {
            if(keep) {
                this.speed += force;
            }
            else {
                this.speed = force;
            }
            if(this.speed > maxSpeed) {
                this.speed = maxSpeed;
            }
            this.posY += speed;
        }

        boolean checkCollide(List<Tube> tubes) {
            if(this.posY < 0 || this.posY + size > mapSizeY) return true;
            for(Tube tube : tubes) {
                if(this.posX + size > tube.pos && this.posX < tube.pos + width)
                    if(this.posY < tube.height || this.posY + size > tube.height + gapSize)
                        return true;
            }
            return false;
        }
    }
    class FlappyEnv {
        int tubeInterval = 30;
        int gravity = 1;
        int jumpForce = -5;
        Random rnd;
        Bird bird;
        int stepCounter;
        List<Tube> tubes = new ArrayList<>();
        boolean done;

        public FlappyEnv() {
            reset();
        }

        public int[] getActionSpace() {
            return new int[]{0, 1};
        }
        public int[][] getObservationSpace() {
            return new int[][]{
                    {-1, mapSizeY - size + 1},
                    {-maxSpeed, maxSpeed},
                    {-(width + 1), mapSizeX},
                    {heightRange[0], heightRange[1]}
            };
        }
        public int[] getObservationSpaceSize() {
            int[][] observationSpace = getObservationSpace();
            return new int[] {
                    observationSpace[0][1] - observationSpace[0][0] +1,
                    observationSpace[1][1] - observationSpace[1][0] +1,
                    observationSpace[2][1] - observationSpace[2][0] +1,
                    observationSpace[3][1] - observationSpace[3][0] +1
            };
        }

        public FlappyAgent.StateDTO state() {
            Tube lastTube = this.tubes.stream().sorted(Comparator.comparingInt(o -> o.pos)).collect(Collectors.toList()).get(0);

            int currentBirdPos;
            if(this.bird.posY < 0) currentBirdPos = -1;
            else if(this.bird.posY > mapSizeY - size) currentBirdPos = mapSizeY - size + 1;
            else currentBirdPos = this.bird.posY;

            currentBirdPos+= 1;
            int currentBirdVel = this.bird.speed + maxSpeed;
            int currentTubeDistance = lastTube.distanceToBird(this.bird) + width + 1;
            int currentTubeHeight = lastTube.height - heightRange[0];

            return new FlappyAgent.StateDTO(currentBirdPos, currentBirdVel, currentTubeDistance, currentTubeHeight);
        }

        private void spawnTube() {
            int tubeHeight = this.rnd.nextInt(heightRange[1] - heightRange[0]) + heightRange[0];
            this.tubes.add(new Tube(mapSizeX, tubeHeight));
        }

        private boolean validAction(int action) {
            for(int a : getActionSpace()) {
                if(a == action)
                    return true;
            }
            return false;
        }

        public ObservationDTO step(int action) {
            if(!validAction(action)) {
                return null;
            }
            int reward = 0;
            if(!this.done) {
                this.stepCounter += 1;
                if(action == 0) {
                    this.bird.step(gravity, true);
                }
                else if(action == 1) {
                    this.bird.step(jumpForce, false);
                }

                if(this.stepCounter % tubeInterval == 0) {
                    spawnTube();
                }

                for(Tube t: this.tubes) {
                    t.step();

                    if(t.pos + width < this.bird.posX && !t.scored) {
                        t.scored = true;
                        reward = 1;
                    }
                }
                this.tubes = this.tubes.stream().filter(tube -> !tube.scored).collect(Collectors.toList());

                if(this.bird.checkCollide(this.tubes)) {
                    reward = -1;
                    this.done = true;
                }
            }

            InfoDTO info = new InfoDTO(this.bird.posX, this.bird.posY, size, this.tubes, width, gapSize);
            ObservationDTO result = new ObservationDTO(state(), reward, done, info);

            return result;
        }

        public ObservationDTO reset() {
            this.rnd = new Random(seed);
            this.bird = new Bird(10, mapSizeY / 2);
            this.stepCounter = 0;
            this.tubes.clear();
            spawnTube();
            this.done = false;

            InfoDTO info = new InfoDTO(this.bird.posX, this.bird.posY, size, this.tubes, width, gapSize);
            ObservationDTO result = new ObservationDTO(state(), 0, done, info);
            return result;
        }

    }

    // DTOs
    class InfoDTO {
        public int birdX;
        public int birdY;
        public int birdSize;
        public List<Tube> tubes;
        public int tubeWidth;
        public int tubeGapsize;

        public InfoDTO() {
        }

        public InfoDTO(int birdX, int birdY, int birdSize, List<Tube> tubes, int tubeWidth, int tubeGapsize) {
            this.birdX = birdX;
            this.birdY = birdY;
            this.birdSize = birdSize;
            this.tubes = tubes;
            this.tubeWidth = tubeWidth;
            this.tubeGapsize = tubeGapsize;
        }

        @Override
        public String toString() {
            return "InfoDTO{" +
                    "birdX=" + birdX +
                    ", birdY=" + birdY +
                    ", birdSize=" + birdSize +
                    ", tubes=" + tubes +
                    ", tubeWidth=" + tubeWidth +
                    ", tubeGapsize=" + tubeGapsize +
                    '}';
        }
    }
    class ObservationDTO {
        public FlappyAgent.StateDTO state;
        public int reward;
        public boolean done;
        public InfoDTO info;

        public ObservationDTO() {
        }

        public ObservationDTO(FlappyAgent.StateDTO state, int reward, boolean done, InfoDTO info) {
            this.state = state;
            this.reward = reward;
            this.done = done;
            this.info = info;
        }

        @Override
        public String toString() {
            return "ObservationDTO{" +
                    "state=" + state +
                    ", reward=" + reward +
                    ", done=" + done +
                    ", info=" + info +
                    '}';
        }
    }

    // Evaluator
    int nIterations = (int) 2e5;
    int iteration = 0;
    int epoch = 0;

    FlappyEnv env = new FlappyEnv();
    FlappyAgent agent = new FlappyAgent(env.getObservationSpaceSize(), env.getActionSpace(), nIterations);

    public void run() {
        while (iteration < nIterations) {
            ObservationDTO observation = env.reset();

            int epochRewardSum = 0;
            boolean done = false;

            while (!done) {
                int action = agent.step(observation.state);
                ObservationDTO newObservation = env.step(action);
                agent.learn(observation.state, action, newObservation.state, newObservation.reward);

                observation = newObservation;

                epochRewardSum += observation.reward;
                done = observation.done;

                iteration += 1;
            }
            agent.epochEnd(epochRewardSum);

            epoch += 1;
        }
        agent.trainEnd();

        int nMaxReward = 25;
        int rewardSum = 0;

        boolean done = false;
        ObservationDTO observation = env.reset();

        while (!done && rewardSum < nMaxReward) {
            int action = agent.step(observation.state);
            ObservationDTO newObservation = env.step(action);
            rewardSum += newObservation.reward;
            done = newObservation.done;
            observation = newObservation;
        }
        System.out.println(rewardSum);
    }

    public static void main(String[] args) {
        FlappyEvaluator flappyEvaluator = new FlappyEvaluator();
        flappyEvaluator.run();
    }
}
