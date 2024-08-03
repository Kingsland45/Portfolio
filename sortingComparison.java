import java.util.Arrays;
import java.util.Random;
import java.util.Scanner;

/**
 * Austin Kingsland
 * 
 * This program demonstrates the use of various sorting algorithms 
 * and allows the user to compare their execution times. 
 * The sorting algorithms included are Quick Sort, Merge Sort, Heap Sort, 
 * Tim Sort (Java's built-in sort), and Intro Sort. 
 * 
 * 
 * The execution time for each sorting algorithm is measured and printed to the console 
 * in nanoseconds. This program showcases an understanding of algorithmic complexity 
 * and performance measurement.
 */

public class SortingComparison {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        // Greet the user
        System.out.println("Welcome to the Sorting Algorithm Comparison Program!");
        
        // Prompt the user for input
        System.out.println("Please choose a sorting algorithm:");
        System.out.println("1. Quick Sort");
        System.out.println("2. Merge Sort");
        System.out.println("3. Heap Sort");
        System.out.println("4. Tim Sort");
        System.out.println("5. Intro Sort");
        System.out.println("6. Run all sorts");
        System.out.print("Enter your choice (1-6): ");
        
        int choice = scanner.nextInt();
        
        // Size of the array to be sorted
        int arraySize = 10000;
        int[] array = new int[arraySize];
        Random random = new Random();
        
        // Populate the array with random integers
        for (int i = 0; i < arraySize; i++) {
            array[i] = random.nextInt(arraySize);
        }
        
        // Copy of the array to be used for sorting
        int[] arrayCopy;
        long startTime, endTime;

        // Switch statement to handle user choice
        switch (choice) {
            case 1:
                // Quick Sort
                arrayCopy = Arrays.copyOf(array, array.length);
                startTime = System.nanoTime();
                quickSort(arrayCopy, 0, arrayCopy.length - 1);
                endTime = System.nanoTime();
                System.out.println("Quick Sort execution time: " + (endTime - startTime) + " ns");
                break;
            case 2:
                // Merge Sort
                arrayCopy = Arrays.copyOf(array, array.length);
                startTime = System.nanoTime();
                mergeSort(arrayCopy, 0, arrayCopy.length - 1);
                endTime = System.nanoTime();
                System.out.println("Merge Sort execution time: " + (endTime - startTime) + " ns");
                break;
            case 3:
                // Heap Sort
                arrayCopy = Arrays.copyOf(array, array.length);
                startTime = System.nanoTime();
                heapSort(arrayCopy);
                endTime = System.nanoTime();
                System.out.println("Heap Sort execution time: " + (endTime - startTime) + " ns");
                break;
            case 4:
                // Tim Sort (Java's built-in sort)
                arrayCopy = Arrays.copyOf(array, array.length);
                startTime = System.nanoTime();
                Arrays.sort(arrayCopy);
                endTime = System.nanoTime();
                System.out.println("Tim Sort execution time: " + (endTime - startTime) + " ns");
                break;
            case 5:
                // Intro Sort
                arrayCopy = Arrays.copyOf(array, array.length);
                startTime = System.nanoTime();
                introSort(arrayCopy, 0, arrayCopy.length - 1, 2 * (int)(Math.log(arrayCopy.length) / Math.log(2)));
                endTime = System.nanoTime();
                System.out.println("Intro Sort execution time: " + (endTime - startTime) + " ns");
                break;
            case 6:
                // Run all sorting algorithms
                arrayCopy = Arrays.copyOf(array, array.length);
                startTime = System.nanoTime();
                quickSort(arrayCopy, 0, arrayCopy.length - 1);
                endTime = System.nanoTime();
                System.out.println("Quick Sort execution time: " + (endTime - startTime) + " ns");

                arrayCopy = Arrays.copyOf(array, array.length);
                startTime = System.nanoTime();
                mergeSort(arrayCopy, 0, arrayCopy.length - 1);
                endTime = System.nanoTime();
                System.out.println("Merge Sort execution time: " + (endTime - startTime) + " ns");

                arrayCopy = Arrays.copyOf(array, array.length);
                startTime = System.nanoTime();
                heapSort(arrayCopy);
                endTime = System.nanoTime();
                System.out.println("Heap Sort execution time: " + (endTime - startTime) + " ns");

                arrayCopy = Arrays.copyOf(array, array.length);
                startTime = System.nanoTime();
                Arrays.sort(arrayCopy);
                endTime = System.nanoTime();
                System.out.println("Tim Sort execution time: " + (endTime - startTime) + " ns");

                arrayCopy = Arrays.copyOf(array, array.length);
                startTime = System.nanoTime();
                introSort(arrayCopy, 0, arrayCopy.length - 1, 2 * (int)(Math.log(arrayCopy.length) / Math.log(2)));
                endTime = System.nanoTime();
                System.out.println("Intro Sort execution time: " + (endTime - startTime) + " ns");
                break;
            default:
                // Handle invalid input
                System.out.println("Invalid choice. Please run the program again and choose a valid option.");
                break;
        }
        
        scanner.close();
    }
    
    // Quick Sort implementation
    public static void quickSort(int[] array, int low, int high) {
        if (low < high) {
            int pi = partition(array, low, high);
            quickSort(array, low, pi - 1);
            quickSort(array, pi + 1, high);
        }
    }
    
    public static int partition(int[] array, int low, int high) {
        int pivot = array[high];
        int i = (low - 1);
        for (int j = low; j < high; j++) {
            if (array[j] <= pivot) {
                i++;
                int temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }
        }
        int temp = array[i + 1];
        array[i + 1] = array[high];
        array[high] = temp;
        return i + 1;
    }
    
    // Merge Sort implementation
    public static void mergeSort(int[] array, int left, int right) {
        if (left < right) {
            int mid = (left + right) / 2;
            mergeSort(array, left, mid);
            mergeSort(array, mid + 1, right);
            merge(array, left, mid, right);
        }
    }
    
    public static void merge(int[] array, int left, int mid, int right) {
        int n1 = mid - left + 1;
        int n2 = right - mid;
        
        int[] L = new int[n1];
        int[] R = new int[n2];
        
        for (int i = 0; i < n1; ++i) {
            L[i] = array[left + i];
        }
        for (int j = 0; j < n2; ++j) {
            R[j] = array[mid + 1 + j];
        }
        
        int i = 0, j = 0;
        int k = left;
        while (i < n1 && j < n2) {
            if (L[i] <= R[j]) {
                array[k] = L[i];
                i++;
            } else {
                array[k] = R[j];
                j++;
            }
            k++;
        }
        
        while (i < n1) {
            array[k] = L[i];
            i++;
            k++;
        }
        
        while (j < n2) {
            array[k] = R[j];
            j++;
            k++;
        }
    }
    
    // Heap Sort implementation
    public static void heapSort(int[] array) {
        int n = array.length;
        
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(array, n, i);
        }
        
        for (int i = n - 1; i > 0; i--) {
            int temp = array[0];
            array[0] = array[i];
            array[i] = temp;
            heapify(array, i, 0);
        }
    }
    
    public static void heapify(int[] array, int n, int i) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        
        if (left < n && array[left] > array[largest]) {
            largest = left;
        }
        
        if (right < n && array[right] > array[largest]) {
            largest = right;
        }
        
        if (largest != i) {
            int swap = array[i];
            array[i] = array[largest];
            array[largest] = swap;
            heapify(array, n, largest);
        }
    }
    
    // Intro Sort implementation
    public static void introSort(int[] array, int low, int high, int depthLimit) {
        if (high - low > 16) {
            if (depthLimit == 0) {
                heapSort(array, low, high);
                return;
            }
            int pivot = partition(array, low, high);
            introSort(array, low, pivot - 1, depthLimit - 1);
            introSort(array, pivot + 1, high, depthLimit - 1);
        } else {
            insertionSort(array, low, high);
        }
    }
    
    public static void heapSort(int[] array, int low, int high) {
        int n = high - low + 1;
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(array, low, high, i);
        }
        for (int i = n - 1; i > 0; i--) {
            int temp = array[low];
            array[low] = array[low + i];
            array[low + i] = temp;
            heapify(array, low, low + i - 1, 0);
        }
    }
    
    public static void heapify(int[] array, int low, int high, int i) {
        int largest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        if (left <= high - low && array[low + left] > array[low + largest]) {
            largest = left;
        }
        if (right <= high - low && array[low + right] > array[low + largest]) {
            largest = right;
        }
        if (largest != i) {
            int swap = array[low + i];
            array[low + i] = array[low + largest];
            array[low + largest] = swap;
            heapify(array, low, high, largest);
        }
    }
    
    // Insertion Sort implementation for small arrays
    public static void insertionSort(int[] array, int low, int high) {
        for (int i = low + 1; i <= high; i++) {
            int key = array[i];
            int j = i - 1;
            while (j >= low && array[j] > key) {
                array[j + 1] = array[j];
                j = j - 1;
            }
            array[j + 1] = key;
        }
    }
}
