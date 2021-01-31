using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InsLabelController : MonoBehaviour
{
	public GameObject cam;
	private const float sensitivity = 5f;
	private Vector2 currentRotation;
	// Start is called before the first frame update
	void Start()
	{
		currentRotation = new Vector2(cam.transform.rotation.y, cam.transform.rotation.x);
		currentRotation.x += 45f;
		currentRotation.x = Mathf.Repeat(currentRotation.x, 360);
	}

	// Update is called once per frame
	void Update()
	{
		if (Input.GetButton("Fire1")) {
			currentRotation.x += Input.GetAxis("Mouse X") * sensitivity;
			currentRotation.x = Mathf.Repeat(currentRotation.x, 360);
			currentRotation.y -= Input.GetAxis("Mouse Y") * sensitivity;
			currentRotation.y = Mathf.Repeat(currentRotation.y, 360);
		}

		if (currentRotation.y > 75 && currentRotation.y < 270) {
			currentRotation.y = 75;
		}
		if (currentRotation.y >= 270 && currentRotation.y <= 360) {
			currentRotation.y = 0;
		}

		transform.rotation = Quaternion.Euler(currentRotation.y, currentRotation.x, 0);

	}
}
