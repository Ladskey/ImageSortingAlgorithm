package sorting.visualizer;

import java.awt.Canvas;
import java.awt.image.DataBufferInt;
import java.util.ArrayList;
import java.util.Collections;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.image.BufferStrategy;
import java.awt.image.BufferedImage;
import javax.swing.JFrame;
import sorting.visualizer.graphics.Picture;
import sorting.visualizer.sorting.MasterSorter;
import sorting.visualizer.sorting.Pixel;
import sorting.visualizer.sorting.SortingMethod;



public class Display extends Canvas implements Runnable {
	private static final long serialVersionUID = 1L;
	private JFrame frame;
	private Thread thread;
	private static String title = "Sorting Algorithm Visualizer";
	private int width = 1280;
	private int height = 720;
	private boolean running = false;
	boolean sorted = false;
	private Picture picture;
	
	private BufferedImage image;
	private int[] pixels;
	private Pixel[] myPixels;
	

	public Display() {
		frame = new JFrame();
		
		picture = new Picture("/images/elmur.jpg"); 
		
		width = picture.getWidth();
		height = picture.getHeight();
		
		image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
		pixels = ((DataBufferInt) image.getRaster().getDataBuffer()).getData();
		myPixels = new Pixel[width * height];
		
		//Creates dimension size and applies it to Canvas
		Dimension size = new Dimension(400, (int) (400.0/width * height));
		this.setPreferredSize(size);
		
		initPixels();
		
	}
	
	
	private void initPixels() {
		for(int i = 0; i < myPixels.length; i++) {
			myPixels[i] = new Pixel(picture.getPixels()[i], i);
		}
		
		randomize();
	}
	
	
	private void randomize() {
		ArrayList<Pixel> pixelList = new ArrayList<Pixel>();
		
		for(int i = 0; i < myPixels.length; i++) {
			pixelList.add(myPixels[i]);
		}
		
		Collections.shuffle(pixelList);
		
		for(int i = 0; i < myPixels.length; i++) {
			myPixels[i] = pixelList.get(i);
		}
	}
	
	
	//Some stuff to make the display work
	public static void main(String[] args) {
		Display display = new Display();
		display.frame.setTitle(title);
		display.frame.add(display);
		display.frame.pack();
		display.frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		display.frame.setLocationRelativeTo(null);
		display.frame.setVisible(true);
		
		display.start();
		
	}
	
	
	//When these methods [start() + stop()] are called, the running variable is set to true/false
	public synchronized void start() {
		running = true;
		
		//Creates new thread and starts it
		thread = new Thread(this, "Display");
		thread.start();
	}

	public synchronized void stop() {
		running = false;
		
		//Joins thread back to current thread
		try {
			thread.join();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	
	@Override
	public void run() {
		//Every time run() loop is called, we get the current time in nanoseconds. 
		// That is compared to the previous time to see how many nanoseconds have passed. 
		long lastTime = System.nanoTime();
		long timer = System.currentTimeMillis();
		//[ns] finds how long update() needs to wait in order to stay at the target frame rate. 
		// The denominator is the frame rate, because it finds that there are 100 sets of 10 million nanoseconds per second, 
		//so update() must wait 10 million nanoseconds before being called again to stay at 100 frames per second.
		// It is set to 400 fps because 100 fps was way too slow.
		final double ns = 1000000000.0 / 400;
		double delta = 0;
		int frames = 0;
		
		//When thread starts and [running = true], this method is called and renders everything to the screen
		// Every time we run, this loop is called
		while(running) {
			//Constantly looks at the difference between [now and lastTime], which is divided by [ns] to get a percentage
			// and when that percentage reaches 100%, update() is called again.
			long now = System.nanoTime();
			delta += (now - lastTime) / ns;
			
			lastTime = now;
			while(delta >= 1) {
				update();
				delta--;
			}
			render();
			frames++;
			
			//Once there is a one second difference between the start of the program and now, then title is updated w/ fps count.  
			if(System.currentTimeMillis() - timer >= 1000) {
				timer += 1000;
				frame.setTitle(title + " | " + frames + " fps");
				frames = 0;
			}
		}
	}
	
	//This draws everything to the screen
	private void render() {
		BufferStrategy bs = this.getBufferStrategy();
		if(bs == null) {
			this.createBufferStrategy(3);
			return;
		}
		
		for(int i = 0; i < pixels.length; i++) {
			pixels[i] = myPixels[i].color;
		}
		
		Graphics g = bs.getDrawGraphics();
		g.drawImage(image, 0, 0, getWidth(), getHeight(), null);
		g.dispose();
		bs.show();
	}
	
	
	//This is where all the logic for the program is
	private void update() {
		if(!sorted) {
			sorted = MasterSorter.sort(myPixels, SortingMethod.BubbleSort, 100000);
		}
	}
	
}
