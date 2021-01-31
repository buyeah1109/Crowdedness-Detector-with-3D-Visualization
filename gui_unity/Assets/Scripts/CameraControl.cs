using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CameraControl : MonoBehaviour
{

	public GameObject lighting;
	public GameObject mall;
	public Text tx;
	private Camera cam;

	private const float magnifyUpper = 18f;
	private const float magnifyLower = 11f;
	private const float sensitivity = 5f;
	private const float camDist = 25f;
	private float verticalUpper = 10f;
	private float verticalLower = -10f;
	private float camDeviate = -5f;

	private Vector2 currentRotation;
	private float rotatedRadius = 10f;
	private float radius = 17.5f;
	private float verticalOffset = 0f;
	private bool isMouseDown = false;

	private string lastSection = "1_1";
	// Start is called before the first frame update
	void Start()
	{
		cam = GetComponent<Camera>();
		currentRotation = new Vector2(45f, 20f);
	}

	// Update is called once per frame
	void Update()
	{
		rotatedRadius = 10f;

		verticalUpper = magnifyUpper - radius;
		verticalLower = -verticalUpper;
		camDeviate = 0.5f * (magnifyUpper - radius) - 10f;

		if (Input.GetButton("Fire1")) {
			currentRotation.x += Input.GetAxis("Mouse X") * sensitivity;
			currentRotation.x = Mathf.Repeat(currentRotation.x, 360);
			currentRotation.y -= Input.GetAxis("Mouse Y") * sensitivity;
			currentRotation.y = Mathf.Repeat(currentRotation.y, 360);
		}
		else if (Input.GetButton("Fire2")) {
			verticalOffset -= Input.GetAxis("Mouse Y") * sensitivity / 10f;
		}

		radius -= 4 * Input.GetAxis("Mouse ScrollWheel");
		radius = radius > magnifyLower ? radius : magnifyLower;
		radius = radius < magnifyUpper ? radius : magnifyUpper;
		verticalOffset = verticalOffset > verticalLower ? verticalOffset : verticalLower;
		verticalOffset = verticalOffset < verticalUpper ? verticalOffset : verticalUpper;

		if (currentRotation.y > 75 && currentRotation.y < 270) {
			currentRotation.y = 75;
		}
		if (currentRotation.y >= 270 && currentRotation.y <= 360) {
			currentRotation.y = 0;
		}

		rotatedRadius = camDist * Mathf.Cos(currentRotation.y / 180 * Mathf.PI);
		
		transform.rotation = Quaternion.Euler(currentRotation.y, currentRotation.x, 0);
		cam.orthographicSize = radius;
		transform.position =
			new Vector3(
				-rotatedRadius * Mathf.Sin(currentRotation.x / 180 * Mathf.PI),
				camDist * Mathf.Sin(currentRotation.y / 180 * Mathf.PI) + verticalOffset,
				-rotatedRadius * Mathf.Cos(currentRotation.x / 180 * Mathf.PI)
			) +
			new Vector3(
				camDeviate * Mathf.Cos(currentRotation.x / 180 * Mathf.PI),
				0,
				-camDeviate * Mathf.Sin(currentRotation.x / 180 * Mathf.PI)
			);

		lighting.transform.rotation = Quaternion.Euler(30f, currentRotation.x, 0);
		lighting.transform.position = transform.position;

		castRay();
	}

	private void castRay(){
		RaycastHit hit;
		Ray ray = cam.ScreenPointToRay(Input.mousePosition);
		
		string name;

		if (Physics.Raycast(ray, out hit)) {
			name = hit.collider.gameObject.name;
		}
		else {
			name = lastSection;
		}

		int floor = (int)char.GetNumericValue(name[0]) - 1;
		int section = (int)char.GetNumericValue(name[2]) - 1;
		float crowdness = mall.GetComponent<FestivalWalk>().getCrowdness(floor, section) * 5f;
		int crowdIdx = (int)Mathf.Floor(crowdness);
		crowdIdx = crowdIdx < 5 ? crowdIdx : 4;

		string[] floorName = {"LG2", "LG1", "G", "UG", "L1", "L2"};
		string[] crowdName = {"Empty", "Sparse", "Normal", "Crowded", "Overcrowded"};

		string result = "Mall: Festival Walk\nFloor: " + floorName[floor] + "\nSection: " + (section + 1) + "\nCrowdness: " + crowdName[crowdIdx];
		tx.text = result;

		lastSection = name;
	}

	public Vector2 getRotation() {
		return currentRotation;
	}
}
