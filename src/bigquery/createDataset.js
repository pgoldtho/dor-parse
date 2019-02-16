// Imports the Google Cloud client library
const BigQuery = require('@google-cloud/bigquery');

// Your Google Cloud Platform project ID
const projectId = 'florida-data';

// Creates a client
const bigquery = new BigQuery({
  projectId: projectId,
});

// The name for the new dataset
const datasetName = 'my_new_dataset';

// Creates the new dataset
bigquery
  .createDataset(datasetName)
  .then(results => {
    const dataset = results[0];

    console.log(`Dataset ${dataset.id} created.`);
  })
  .catch(err => {
    console.error('ERROR:', err);
  });
