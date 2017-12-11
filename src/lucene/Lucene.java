

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class Lucene {
	private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

	private IndexWriter writer;
	private ArrayList<File> queue = new ArrayList<File>();
	private static int maxLimit = 100;

	public static void main(String[] args) throws IOException {
		
		System.out.println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");

		String indexLocation = null;
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		String s = br.readLine();

		Lucene indexer = null;
		try {
			indexLocation = s;
			indexer = new Lucene(s);
		} catch (Exception ex) {
			System.out.println("Cannot create index..." + ex.getMessage());
			System.exit(-1);
		}

		// ===================================================
		// read input from user until he enters q for quit
		// ===================================================
		while (!s.equalsIgnoreCase("q")) {
			try {
				System.out.println(
						"Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
				System.out.println("[Acceptable file types: .xml, .html, .html, .txt]");
				s = br.readLine();
				if (s.equalsIgnoreCase("q")) {
					break;
				}

				// try to add file into the index
				indexer.indexFileOrDirectory(s);
			} catch (Exception e) {
				System.out.println("Error indexing " + s + " : " + e.getMessage());
			}
		}

		// ===================================================
		// after adding, we always have to call the
		// closeIndex, otherwise the index is not created
		// ===================================================
		indexer.closeIndex();

		// =========================================================
		// Now search
		// =========================================================
		IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(indexLocation)));
		IndexSearcher searcher = new IndexSearcher(reader);
		
		System.out.println("Enter the FULL path to the query file with .txt extension (Where to read queries from) :");
		String queryFilePath = br.readLine();
		HashMap<Integer, String> queries =  readQueriesFromFile(queryFilePath);
		System.out.println("...........................");
		System.out.println(queries.size());
		
		String systemName = " Lucene_Simple_Analyzer\n";
		
		System.out.println("Enter the FULL path to the scores file with .txt extension (Where final scores will be stored) :");
		String scoreFileName = br.readLine();
		BufferedWriter writer = new BufferedWriter(new FileWriter(scoreFileName));
		
		for (Map.Entry<Integer, String> entry : queries.entrySet()) {
			int key = entry.getKey();
			String query = entry.getValue();
			
			TopScoreDocCollector collector = TopScoreDocCollector.create(maxLimit, true);
			
			try {
				String escapedQuery = query.replace("--", "");
				Query q = new QueryParser(Version.LUCENE_47, "contents", sAnalyzer).parse(escapedQuery);
				searcher.search(q, collector);
				ScoreDoc[] hits = collector.topDocs().scoreDocs;

				// 4. display results
				System.out.println("Found " + hits.length + " hits.");
				for (int i = 0; i < hits.length; ++i) {
					int docId = hits[i].doc;
					Document d = searcher.doc(docId);
					System.out.println((i + 1) + ". " + d.get("path") + " score=" + hits[i].score);
					
					// score response format
					// query_id Q0 doc_id rank BM25_score system_name
					
					File f = new File(d.get("path"));
					
					writer.write(key + " Q0 " + f.getName().replace(".txt", "") + " " + (i+1) + " " + hits[i].score + systemName);
					
				}
				writer.write("\n");
				// 5. term stats --> watch out for which "version" of the term
				// must be checked here instead!
				for (String queryWord: query.split(" ")) {
					Term termInstance = new Term("contents", queryWord);
					long termFreq = reader.totalTermFreq(termInstance);
					long docCount = reader.docFreq(termInstance);
					System.out.println(queryWord + " Term Frequency " + termFreq + " - Document Frequency " + docCount);
				}

			} catch (Exception e) {
				System.out.println("Error searching " + s + " : " + e.getMessage());
				break;
			}
			
		}
		
		writer.close();

	}
	
	public static HashMap<Integer, String> readQueriesFromFile(String queryFile) {
		HashMap<Integer, String> queries = new HashMap<Integer, String>();
		
		String line = null;
		try {
			FileReader fileReader = new FileReader(queryFile);
			BufferedReader bufferedReader = new BufferedReader(fileReader);
			int count = 0;
			while((line = bufferedReader.readLine()) != null) {
				count++;
				queries.put(count, line.trim());
            }
			
			bufferedReader.close();
			
		} catch(Exception ex) {
			System.out.println("Error\n" + ex);
		}
		return queries;
	}
	
	
	/**
	 * Constructor
	 * 
	 * @param indexDir
	 *            the name of the folder in which the index should be created
	 * @throws java.io.IOException
	 *             when exception creating index.
	 */
	Lucene(String indexDir) throws IOException {

		FSDirectory dir = FSDirectory.open(new File(indexDir));

		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47, sAnalyzer);

		writer = new IndexWriter(dir, config);
	}

	/**
	 * Indexes a file or directory
	 * 
	 * @param fileName
	 *            the name of a text file or a folder we wish to add to the index
	 * @throws java.io.IOException
	 *             when exception
	 */
	public void indexFileOrDirectory(String fileName) throws IOException {
		// ===================================================
		// gets the list of files in a folder (if user has submitted
		// the name of a folder) or gets a single file name (is user
		// has submitted only the file name)
		// ===================================================
		addFiles(new File(fileName));

		int originalNumDocs = writer.numDocs();
		for (File f : queue) {
			FileReader fr = null;
			try {
				Document doc = new Document();

				// ===================================================
				// add contents of file
				// ===================================================
				fr = new FileReader(f);
				doc.add(new TextField("contents", fr));
				doc.add(new StringField("path", f.getPath(), Field.Store.YES));
				doc.add(new StringField("filename", f.getName(), Field.Store.YES));

				writer.addDocument(doc);
				System.out.println("Added: " + f);
			} catch (Exception e) {
				System.out.println("Could not add: " + f);
			} finally {
				fr.close();
			}
		}

		int newNumDocs = writer.numDocs();
		System.out.println("");
		System.out.println("************************");
		System.out.println((newNumDocs - originalNumDocs) + " documents added.");
		System.out.println("************************");

		queue.clear();
	}

	private void addFiles(File file) {

		if (!file.exists()) {
			System.out.println(file + " does not exist.");
		}
		if (file.isDirectory()) {
			for (File f : file.listFiles()) {
				addFiles(f);
			}
		} else {
			String filename = file.getName().toLowerCase();
			// ===================================================
			// Only index text files
			// ===================================================
			if (filename.endsWith(".htm") || filename.endsWith(".html") || filename.endsWith(".xml")
					|| filename.endsWith(".txt")) {
				queue.add(file);
			} else {
				System.out.println("Skipped " + filename);
			}
		}
	}

	/**
	 * Close the index.
	 * 
	 * @throws java.io.IOException
	 *             when exception closing
	 */
	public void closeIndex() throws IOException {
		writer.close();
	}
}

// Index Folder
// /Users/exmachina/Northeastern/classes/IR/Assignments/hw4/index
// Documents folder (parsed)
// /Users/exmachina/Northeastern/classes/IR/Assignments/hw4/documents
// Queries path
// /Users/exmachina/Northeastern/classes/IR/Assignments/hw4/queries.txt
// Scores path
// /Users/exmachina/Northeastern/classes/IR/Assignments/hw4/scores.txt
