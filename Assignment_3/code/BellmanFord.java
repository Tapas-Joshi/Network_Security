import java.io.*;
import java.util.*;
import java.text.SimpleDateFormat;

public class BellmanFord extends Thread {
    private static final String Input_File = "/Users/Tapas/Documents/input";
    public static int g = 0;
    public static int[] integers = new int[100];
    public static boolean attack, hasRead;
    static SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss");

    static {
        hasRead = false;
    }

    final int INFINITY = 999;
    public HashMap<Integer, Integer> dest_cost = new HashMap<Integer, Integer>();
    public BufferedReader inp = new BufferedReader(new InputStreamReader(System.in));
    LinkedList<Edge> edges;
    int d[], p[], x[];
    int nextHop[] = new int[100];
    int n, e, s, l = 0;

    @Override
    public void run() {
        int i = 0;
        //   System.out.println("This is thread "+ Thread.currentThread().getName());

        if (currentThread().getName().equals("Input_Thread")) {
            try {
                System.out.print("Enter (Y/y) to Attack:");
                Scanner s = new Scanner(System.in);
                char x = s.next().charAt(0);
                if (x == 'Y' || x == 'y') {
                    attack = true;
                    attack();
                }
                while (i < 7) {
                    BF(i);
                    i++;
                }
            } catch (IOException e1) {
                e1.printStackTrace();
            } catch (InterruptedException e1) {
                e1.printStackTrace();
            }
        }

        while (!attack) {

            for (int k = 0; k < 7; k++) {

                if (currentThread().getName().equals(Integer.toString(k))) {
                    try {
                        this.BF(k);

                    } catch (IOException e1) {
                        e1.printStackTrace();
                    } catch (InterruptedException e1) {
                        e1.printStackTrace();
                    }
                }

            }
            try {
                // attack();
                sleep(10000);

            } catch (InterruptedException e1) {
                e1.printStackTrace();
            }

        }

        //  System.out.println("Thread ended: " + Thread.currentThread().getName());

    }

    public void BF(int k) throws IOException, InterruptedException {


        if (!currentThread().getName().equals("Input_Thread")) {
            sleep(k * 100);
        }

        System.out.println("Thread " + currentThread().getName() + " for node " + k + ". Broadcasting...\nUpdating Tables Every 10 seconds....");
        int item;
        edges = new LinkedList<Edge>();
        //  inp = new BufferedReader (new InputStreamReader(System.in));

        //System.out.print("Enter number of vertices ");
        // n = Integer.parseInt(inp.readLine());
        n = 7;

        if (!hasRead) {
            System.out.println("Reading input file...");
            FileReader file = new FileReader(Input_File);
            l = 0;
            try {
                Scanner input = new Scanner(file);
                while (input.hasNext()) {
                    integers[l] = input.nextInt();
                    l++;
                }
                input.close();
                l = 0;
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        l = 0;
        //   System.out.println("Cost Matrix");
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                item = integers[l];
                // System.out.println("Value of l is "+l + "Integer "+ integers[l]);
                l++;
                if (item != 0)
                    edges.add(new Edge(i, j, item));
            }
        }

        e = edges.size();
        d = new int[n];
        p = new int[n];
        x = new int[n];

        //    System.out.print("Enter the source vertex ");
        //    s = Integer.parseInt(inp.readLine());

        int i, j;
        for (i = 0; i < n; ++i) {
            d[i] = INFINITY;
            p[i] = -1;

        }
        s = k;
        d[s] = 0;
        for (i = 0; i < n - 1; ++i) {
            for (j = 0; j < e; ++j) { //here i am calculating the shortest path
                if (d[edges.get(j).u] + edges.get(j).w < d[edges.get(j).v]) {
                    d[edges.get(j).v] = d[edges.get(j).u] + edges.get(j).w;
                    //    System.out.println(edges.get(j).u+"--->"+edges.get(j).v + "=="+ edges.get(j).w);
                    //p[edges.get(j).v] = edges.get(j).u;
                    p[edges.get(j).v] = edges.get(j).u;
                    //  System.out.println(edges.get(j).u);
                }
            }
            //     System.out.println("For Destination="+i);
        }

        //     nextHop(k);

        for (int m = 0; m < n; m++) {
            dest_cost.put(m, p[m]);
            //   System.out.println(dest_cost);
            //    System.out.println("Vertex " + i + " has predecessor " + p[i]);
        }
        int dest = 0, pred = 0;

        for (int h = 0; h < n; h++) {
            dest = h;
            pred = dest_cost.get(h);

            while (pred != k && dest != -1) { //Check whether the predecesor is not the source

                dest = pred;
                if (dest != -1) {
                    //     System.out.print(dest+ "-");
                    pred = dest_cost.get(dest);
                }
            }
            //  dest=0;
            nextHop[h] = dest;
            // System.out.println("Next Hop For destination: "+h +":-->"+ nextHop[h]);

        }

        if (cycle()) {
            System.out.println("Source\tDestination\tNextHop\tCost\tTime");
            for (int o = 0; o < n; o++) {
                //      System.out.println(r.s + " ==> " + i + " == " + r.d[i]);
                //     System.out.println(k + " ==> " + r.d[i]);

                System.out.println("  " + s + "\t\t\t" + o + " \t\t " + nextHop[o] + "\t\t " + d[o] + "\t  " + sdf.format(new Date()));
                x[o] = d[o];
            }
            System.out.println("-------------------------------------------");
        } else {
            System.out.println(" There is a negative edge cycle ");
        }

        //System.out.println("Thread killed: "+Thread.currentThread().getName());
        //Thread.currentThread().stop();

        if (currentThread().getName().equals("6")) {
            System.out.println("Has read turned true");
            hasRead = true;
            System.out.print("Enter (Y/y) to Attack: ");
        }
    }

    boolean cycle() {
        int j;
        for (j = 0; j < e; ++j)
            if (d[edges.get(j).u] + edges.get(j).w < d[edges.get(j).v])
                return false;
        return true;
    }

    void attack() throws IOException, InterruptedException {

        int[][] attackerArray = new int[100][100];
        int i, j;
        l = 0;
        int src = 0;
        int dest = 0;
        int exploited_edge_weight = 0;
        int attackNode = 0;
        System.out.print("Enter source node to attack: ");
        src = Integer.parseInt(inp.readLine());
        System.out.print("Enter destination node to attack: ");
        dest = Integer.parseInt(inp.readLine());
        System.out.print("Enter the attacker node: ");
        attackNode = Integer.parseInt(inp.readLine());
        System.out.print("Enter the exploited edge weight: ");
        exploited_edge_weight = Integer.parseInt(inp.readLine());
        System.out.println("Attack Node: " + attackNode + " Changed weight: " + src + "-->" + dest + "=" + exploited_edge_weight);


        //Change the value from matrix to the attacker value and then refresh the table (call BF method)

        i = 0;
        while (i < 7) {
            j = 0;
            while (j < 7) {
                attackerArray[i][j] = integers[l];
                l++;
                j++;
            }
            i++;
        }
        l = 0;

        // System.out.println("Attack array["+src+"]["+attackNode+"]="+attackerArray[src][attackNode]);
        attackerArray[src][attackNode] = exploited_edge_weight;
        attackerArray[attackNode][src] = exploited_edge_weight;
        attackerArray[attackNode][dest] = exploited_edge_weight;
        attackerArray[dest][attackNode] = exploited_edge_weight;

        i = 0;
        while (i < 7) {
            j = 0;
            while (j < 7) {
                integers[l] = attackerArray[i][j];
                l++;
                j++;
            }
            i++;
        }
        l = 0;
    }

    private static class Edge {
        int u, v, w;

        public Edge(int a, int b, int c) {
            u = a;
            v = b;
            w = c;
        }
    }
}


class main_nodes {

    public static String threadName;

    public static void main(String[] args) throws IOException, InterruptedException {

        BellmanFord bel = new BellmanFord();
        bel.setName("Input_Thread");
        System.out.println("Input Thread " + bel.getName() + " Started");
        bel.start();

        for (int i = 0; i < 7; i++) {

            BellmanFord bell = new BellmanFord();

            bell.setName(Integer.toString(i));
            System.out.println("Thread " + bell.getName() + " Started");
            threadName = bell.getName();
            bell.start();

            System.out.println("Finished all threads");

        }

    }
}



