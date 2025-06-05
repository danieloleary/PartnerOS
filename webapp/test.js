// Test file loading
async function testFileLoading() {
  console.log('Starting file loading tests...');
  
  // Test 1: Check if file_list.json exists and is valid
  try {
    const response = await fetch('file_list.json');
    if (!response.ok) {
      throw new Error(`file_list.json not found: ${response.status} ${response.statusText}`);
    }
    const fileList = await response.json();
    console.log('✅ file_list.json loaded successfully:', fileList);
    
    // Test 2: Try loading a sample document
    const testDoc = fileList[1]; // Try loading the second document
    console.log('Attempting to load test document:', testDoc);
    
    const docResponse = await fetch(testDoc);
    if (!docResponse.ok) {
      throw new Error(`Test document not found: ${docResponse.status} ${docResponse.statusText}`);
    }
    const docContent = await docResponse.text();
    console.log('✅ Test document loaded successfully:', {
      path: testDoc,
      contentLength: docContent.length,
      preview: docContent.substring(0, 100) + '...'
    });
    
    // Test 3: Verify path resolution
    const pathParts = testDoc.split('/');
    console.log('Path analysis:', {
      fullPath: testDoc,
      parts: pathParts,
      section: pathParts[0],
      filename: pathParts[pathParts.length - 1]
    });
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  }
}

// Run tests when the page loads
window.addEventListener('load', testFileLoading); 