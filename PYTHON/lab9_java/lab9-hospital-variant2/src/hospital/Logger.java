package hospital;

import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

public final class Logger {
    private static final DateTimeFormatter FORMAT = DateTimeFormatter.ofPattern("HH:mm:ss");
    private static LocalTime clock = LocalTime.of(8, 0, 0);

    private Logger() {
    }

    public static synchronized void log(String source, String event) {
        System.out.printf("[%s] [%s] %s%n", clock.format(FORMAT), source, event);
    }

    public static void work(long simulatedSeconds) {
        try {
            Thread.sleep(150);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        tick(simulatedSeconds);
    }

    public static synchronized void tick(long simulatedSeconds) {
        clock = clock.plusSeconds(simulatedSeconds);
    }

    public static synchronized void resetClock(int hour, int minute) {
        clock = LocalTime.of(hour, minute, 0);
    }
}
