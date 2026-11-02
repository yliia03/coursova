package hospital;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashSet;
import java.util.Objects;
import java.util.Optional;
import java.util.Set;

public class UltrasoundPool {
    private final Deque<UltrasoundDevice> available = new ArrayDeque<>();
    private final Set<UltrasoundDevice> inUse = new HashSet<>();
    private int totalCreated = 0;
    private int totalServed = 0;

    public UltrasoundPool(int size) {
        if (size <= 0) {
            throw new IllegalArgumentException("Розмір пулу має бути додатним: " + size);
        }
        Logger.log("Пул УЗД", "Ініціалізація пулу, апаратів: " + size);
        for (int i = 1; i <= size; i++) {
            available.add(new UltrasoundDevice("US-0" + i));
            totalCreated++;
        }
    }

    public synchronized Optional<UltrasoundDevice> acquire(Patient patient, String profile) {
        UltrasoundDevice device = available.poll();
        if (device == null) {
            Logger.log("Пул УЗД", "Усі апарати зайняті, " + patient + " очікує");
            return Optional.empty();
        }
        device.assign(patient, profile);
        inUse.add(device);
        totalServed++;
        Logger.log("Пул УЗД", "Видано " + device.getId() + " для " + patient + " (профіль «" + profile + "»). Вільних: " + available.size());
        return Optional.of(device);
    }

    public synchronized void release(UltrasoundDevice device, Patient patient) {
        Objects.requireNonNull(device, "device");
        if (!inUse.contains(device) || device.getCurrentPatient() != patient) {
            Logger.log("Пул УЗД", "Апарат " + device.getId() + " не можна повернути: " + "він не виданий цьому пацієнту або вже повернений");
            return;
        }
        inUse.remove(device);
        Patient previous = device.getCurrentPatient();
        device.reset();
        available.add(device);
        Logger.log("Пул УЗД", device.getId() + " повернено після " + previous + ", налаштування скинуто. Вільних: " + available.size());
    }

    public synchronized int availableCount() {
        return available.size();
    }

    public synchronized int inUseCount() {
        return inUse.size();
    }

    public synchronized int getTotalCreated() {
        return totalCreated;
    }

    public synchronized int getTotalServed() {
        return totalServed;
    }
}
