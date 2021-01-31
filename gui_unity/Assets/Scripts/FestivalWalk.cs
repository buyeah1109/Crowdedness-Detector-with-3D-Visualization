using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class FestivalWalk : MonoBehaviour
{

	public const int N = 6;
	private const float baseHeight = 0.1f;
	private const float maxHeight = 0.4f;
	public GameObject[] go1;
	public GameObject[] go2;
	public GameObject[] go3;
	public GameObject[] go4;
	public GameObject[] go5;
	public GameObject[] go6;

	private List<GameObject>[] sections = new List<GameObject>[N];
	private List<Material>[] materials = new List<Material>[N];
	private List<float>[] stats = new List<float>[N];
	private List<float>[] statsTar = new List<float>[N];
	private List<float>[] hue = new List<float>[N];
	private List<bool>[] updating = new List<bool>[N];
	// Start is called before the first frame update
	void Start()
	{
		for (int i=0;i<N;i++) {
			sections[i] = new List<GameObject>();
			materials[i] = new List<Material>();
			stats[i] = new List<float>();
			statsTar[i] = new List<float>();
			hue[i] = new List<float>();
			updating[i] = new List<bool>();
		}
		int floor = 0;
		for (int i=0;i<go1.Length;i++) {
			sections[floor].Add(go1[i]);
		}
		floor++;
		for (int i=0;i<go2.Length;i++) {
			sections[floor].Add(go2[i]);
		}
		floor++;
		for (int i=0;i<go3.Length;i++) {
			sections[floor].Add(go3[i]);
		}
		floor++;
		for (int i=0;i<go4.Length;i++) {
			sections[floor].Add(go4[i]);
		}
		floor++;
		for (int i=0;i<go5.Length;i++) {
			sections[floor].Add(go5[i]);
		}
		floor++;
		for (int i=0;i<go6.Length;i++) {
			sections[floor].Add(go6[i]);
		}

		for (int i=0;i<N;i++) {
			for (int j=0;j<sections[i].Count;j++) {
				sections[i][j].GetComponent<MeshRenderer>().material = Object.Instantiate(sections[i][j].GetComponent<MeshRenderer>().material);
				materials[i].Add(sections[i][j].GetComponent<MeshRenderer>().material);
				stats[i].Add(0f);
				statsTar[i].Add(0f);
				hue[i].Add(0.33f);
				updating[i].Add(false);
			}
		}

		getDemoStats();
		getStats();
	}

	// Update is called once per frame
	void Update()
	{
		updateGraphic();
	}

	public void getDemoStats() {

		for (int i=0;i<N;i++) {
			for (int j=0;j<sections[i].Count;j++) {
				statsTar[i][j] = Random.Range(0.0f, 1.0f);
				updating[i][j] = true;
			}
		}

	}

	public void getStats() {

		for (int i=0;i<N;i++) {
			for (int j=0;j<sections[i].Count;j++) {
				StartCoroutine(requestStates(i, j));
			}
		}

	}

	void updateGraphic() {

		for (int i=0;i<N;i++) {
			for (int j=0;j<sections[i].Count;j++) {
				hue[i][j] = 0.33f * (1 - stats[i][j]);
				float targetScale = (baseHeight + maxHeight * stats[i][j]) / (baseHeight + maxHeight);
				sections[i][j].transform.parent.localScale = new Vector3(1f, targetScale * 1.5f, 1f);
				materials[i][j].SetColor("_Color", Color.HSVToRGB(hue[i][j], 1f, 1f));

				if (updating[i][j]) {
					stats[i][j] += (stats[i][j] < statsTar[i][j] ? 1 : -1) * Time.deltaTime;
					if (Mathf.Abs(stats[i][j] - statsTar[i][j]) < 0.001f) {
						stats[i][j] = statsTar[i][j];
						updating[i][j] = false;
					}
				}
			}
		}

	}

	IEnumerator requestStates(int floor, int section)
	{

		string URL = "http://127.0.0.1:5000/data?mall=festivalwalk&floor=" + (floor + 1) + "&section=" + (section + 1);

		UnityWebRequest www = UnityWebRequest.Get(URL);
		
		yield return www.SendWebRequest();

		if (www.isNetworkError || www.isHttpError) {
			Debug.LogError(www.error);
			statsTar[floor][section] = 0f;
		}
		else {
			Debug.Log(www.downloadHandler.text);
			statsTar[floor][section] = int.Parse(www.downloadHandler.text);
			Debug.Log(floor + " " + section + " " + statsTar[floor][section]);
		}

	}

	public float getCrowdness(int floor, int section) {
		return statsTar[floor][section];
	}
}
